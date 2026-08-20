"""
Multiplayer Party Manager & Initiative Turn Order Engine for Agentic D&D.
Handles party roster, active player selection, round-robin turn progression,
and deterministic Initiative tracking for party and monsters.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from tools.state_manager import StateManager
from tools.dice import roll_dice
from tools.formatting import (
    render_hp_bar, box_header, box_section, badge,
    BOLD, RESET, DIM, CYAN, GREEN, YELLOW, BRIGHT_YELLOW, BRIGHT_CYAN
)


class MultiplayerManager:
    def __init__(self, project_root: Optional[str] = None):
        self.sm = StateManager(project_root)

    def get_party(self) -> List[Dict[str, Any]]:
        return self.sm.get_party()

    def get_active_player(self) -> Optional[Dict[str, Any]]:
        """Returns the currently active player character."""
        party = self.get_party()
        if not party:
            return None
        world = self.sm.get_world()
        active_id = world.get("active_character_id")
        if active_id:
            for p in party:
                if p.get("id") == active_id or p.get("name").lower() == active_id.lower():
                    return p
        return party[0]

    def set_active_player(self, character_id_or_name: str) -> Dict[str, Any]:
        """Sets the active player character."""
        party = self.get_party()
        target = None
        clean = character_id_or_name.lower().replace(" ", "_")
        for p in party:
            if p.get("id", "").lower() == clean or p.get("name", "").lower() == character_id_or_name.lower():
                target = p
                break

        if not target:
            return {"success": False, "error": f"Character '{character_id_or_name}' not found in party."}

        world = self.sm.get_world()
        world["active_character_id"] = target.get("id")
        self.sm.save_world(world)

        return {"success": True, "active_character": target}

    def roll_initiative(self, monsters: Optional[List[Dict[str, Any]]] = None, seed: Optional[int] = None) -> Dict[str, Any]:
        """Rolls initiative for party and monsters and stores the order."""
        party = self.get_party()
        combatants = []

        # Party initiative
        for p in party:
            dex = p.get("stats", {}).get("dexterity", 10)
            dex_mod = (dex - 10) // 2
            mod_str = f"+{dex_mod}" if dex_mod >= 0 else str(dex_mod)
            roll_res = roll_dice(f"1d20{mod_str}", seed=seed)
            combatants.append({
                "id": p.get("id"),
                "name": p.get("name"),
                "is_player": p.get("is_player", True),
                "is_monster": False,
                "dex_mod": dex_mod,
                "initiative": roll_res["total"],
                "formula": roll_res["formula"],
                "hp": p.get("hp", {}),
                "ac": p.get("ac", 10)
            })

        # Monster initiative
        if monsters:
            for m in monsters:
                dex = m.get("stats", {}).get("dexterity", 10)
                dex_mod = (dex - 10) // 2
                mod_str = f"+{dex_mod}" if dex_mod >= 0 else str(dex_mod)
                roll_res = roll_dice(f"1d20{mod_str}", seed=seed)
                combatants.append({
                    "id": m.get("id", m.get("name", "monster").lower().replace(" ", "_")),
                    "name": m.get("name"),
                    "is_player": False,
                    "is_monster": True,
                    "dex_mod": dex_mod,
                    "initiative": roll_res["total"],
                    "formula": roll_res["formula"],
                    "hp": m.get("hp", {}),
                    "ac": m.get("ac", 10)
                })

        # Sort descending by initiative, then DEX mod
        combatants.sort(key=lambda x: (x["initiative"], x["dex_mod"]), reverse=True)

        combat_state = {
            "in_combat": True,
            "round": 1,
            "turn_index": 0,
            "order": combatants
        }
        self.sm.save_combat(combat_state)

        return combat_state

    def get_initiative(self) -> Dict[str, Any]:
        """Returns current initiative state."""
        return self.sm.get_combat()

    def advance_turn(self) -> Dict[str, Any]:
        """Advances combat turn order to the next combatant."""
        combat = self.sm.get_combat()
        if not combat.get("in_combat") or not combat.get("order"):
            return {"success": False, "error": "Combat is not active."}

        order = combat["order"]
        cur_idx = combat.get("turn_index", 0)
        cur_round = combat.get("round", 1)

        next_idx = cur_idx + 1
        if next_idx >= len(order):
            next_idx = 0
            cur_round += 1

        combat["turn_index"] = next_idx
        combat["round"] = cur_round
        self.sm.save_combat(combat)

        current_combatant = order[next_idx]

        # If it is a player character, auto-set active player
        if not current_combatant.get("is_monster") and current_combatant.get("is_player"):
            self.set_active_player(current_combatant.get("id"))

        return {
            "success": True,
            "round": cur_round,
            "turn_index": next_idx,
            "current_combatant": current_combatant,
            "combat": combat
        }

    def end_combat(self) -> Dict[str, Any]:
        """Ends combat and clears initiative."""
        combat = {
            "in_combat": False,
            "round": 0,
            "turn_index": 0,
            "order": []
        }
        self.sm.save_combat(combat)
        return {"success": True, "message": "Combat has ended."}

    def add_member(self, character_id_or_name: str) -> Dict[str, Any]:
        """Adds a character from the Character Vault into the current party roster."""
        from tools.vault import CharacterVault
        vault = CharacterVault(str(self.sm.project_root))
        char = vault.get_character(character_id_or_name)
        if not char:
            return {"success": False, "error": f"Character '{character_id_or_name}' not found in vault."}

        party = self.get_party()
        clean_id = char.get("id")
        for p in party:
            if p.get("id") == clean_id:
                return {"success": False, "error": f"Character '{char.get('name')}' is already in the party."}

        party.append(char)
        self.sm.save_party(party)
        return {"success": True, "character": char, "party_size": len(party)}

    def remove_member(self, character_id_or_name: str) -> Dict[str, Any]:
        """Removes a character from the active party (character remains saved in vault)."""
        party = self.get_party()
        clean_id = character_id_or_name.lower().replace(" ", "_").replace("'", "")
        removed = None
        new_party = []
        for p in party:
            if p.get("id", "").lower() == clean_id or p.get("name", "").lower() == character_id_or_name.lower():
                removed = p
            else:
                new_party.append(p)

        if not removed:
            return {"success": False, "error": f"Character '{character_id_or_name}' is not in the party."}

        self.sm.save_party(new_party)
        
        # If removed character was the active player, switch to first available
        active = self.get_active_player()
        if active and active.get("id") == removed.get("id"):
            if new_party:
                self.set_active_player(new_party[0].get("id"))
            else:
                world = self.sm.get_world()
                world.pop("active_character_id", None)
                self.sm.save_world(world)

        return {"success": True, "removed": removed, "party_size": len(new_party)}

    def get_roster_overview(self) -> Dict[str, Any]:
        """Returns active party members alongside available vault characters."""
        from tools.vault import CharacterVault
        vault = CharacterVault(str(self.sm.project_root))
        party = self.get_party()
        vault_all = vault.list_characters()
        party_ids = {p.get("id") for p in party}
        bench = [c for c in vault_all if c.get("id") not in party_ids]

        return {
            "active_party": party,
            "party_count": len(party),
            "bench_vault": bench,
            "vault_count": len(vault_all)
        }

