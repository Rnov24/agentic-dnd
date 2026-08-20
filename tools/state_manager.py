"""
State Management Layer for Agentic D&D.
Handles persistent JSON runtime state, schema validation, and automatic
bi-directional synchronization with human-readable Markdown campaign files.
Loads default state templates dynamically from rules/defaults.json via Compendium.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional
from tools.mechanics import calculate_modifier
from tools.compendium import Compendium


class StateManager:
    """
    Manages structured state in `state/` and markdown knowledge in `campaign/`.
    """

    def __init__(self, base_dir: Optional[str] = None):
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            self.base_dir = Path(__file__).resolve().parent.parent

        self.project_root = self.base_dir if not (self.base_dir.name in ["state", "campaign"]) else self.base_dir.parent
        self.compendium = Compendium.get_instance(self.project_root)

        from tools.run_manager import RunManager
        rm = RunManager(self.project_root)
        self.state_dir, self.campaign_dir = rm.get_active_run_paths()

        self.party_file = self.state_dir / "party.json"
        self.world_file = self.state_dir / "world.json"
        self.combat_file = self.state_dir / "combat.json"
        self.history_file = self.state_dir / "history.json"
        self.npcs_file = self.state_dir / "npcs.json"
        self.quests_file = self.state_dir / "quests.json"
        self.relationships_file = self.state_dir / "relationships.json"
        self.items_file = self.state_dir / "items.json"
        self.locations_file = self.state_dir / "locations.json"
        self.encounters_file = self.state_dir / "encounters.json"
        self.monsters_file = self.state_dir / "monsters.json"

        self._init_files()

    def _init_files(self):
        """Ensure state directory and initial state files exist."""
        self.state_dir.mkdir(parents=True, exist_ok=True)
        self.campaign_dir.mkdir(parents=True, exist_ok=True)

        if not self.party_file.exists():
            self._save_json(self.party_file, {"party": []})

        if not self.world_file.exists():
            default_world = self.compendium.get_defaults("world")
            self._save_json(self.world_file, default_world)

        if not self.combat_file.exists():
            default_combat = self.compendium.get_defaults("combat")
            self._save_json(self.combat_file, default_combat)

        if not self.history_file.exists():
            default_hist = self.compendium.get_defaults("history")
            self._save_json(self.history_file, default_hist)

        if not self.npcs_file.exists():
            self._save_json(self.npcs_file, {"npcs": []})

        if not self.quests_file.exists():
            self._save_json(self.quests_file, {"active_quests": [], "completed_quests": []})

        if not self.relationships_file.exists():
            default_rel = self.compendium.get_defaults("relationships")
            self._save_json(self.relationships_file, default_rel)

    def _load_json(self, file_path: Path) -> Any:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save_json(self, file_path: Path, data: Any):
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # World State
    def get_world_state(self) -> Dict[str, Any]:
        return self._load_json(self.world_file)

    def get_world(self) -> Dict[str, Any]:
        return self.get_world_state()

    def save_world(self, data: Dict[str, Any]) -> None:
        self._save_json(self.world_file, data)

    def update_world_state(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        current = self.get_world_state()
        current.update(updates)
        self._save_json(self.world_file, current)
        return current

    # Combat State
    def get_combat_state(self) -> Dict[str, Any]:
        return self._load_json(self.combat_file)

    def get_combat(self) -> Dict[str, Any]:
        return self.get_combat_state()

    def save_combat(self, data: Dict[str, Any]) -> None:
        self._save_json(self.combat_file, data)

    def update_combat_state(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        current = self.get_combat_state()
        current.update(updates)
        self._save_json(self.combat_file, current)
        return current

    def get_full_state(self) -> Dict[str, Any]:
        """Returns unified snapshot of all state domains."""
        return {
            "world": self.get_world_state(),
            "party": self.get_party(),
            "combat": self.get_combat_state(),
            "npcs": self.get_npcs(),
            "quests": self.get_quests(),
            "relationships": self.get_relationships()
        }

    # Party & Characters
    def get_party(self) -> List[Dict[str, Any]]:
        data = self._load_json(self.party_file)
        return data.get("party", [])

    def save_party(self, party_list: List[Dict[str, Any]]) -> None:
        self._save_json(self.party_file, {"party": party_list})
        for char in party_list:
            self.sync_character_to_markdown(char)

    def get_character(self, character_id_or_name: str) -> Optional[Dict[str, Any]]:
        party = self.get_party()
        target = character_id_or_name.lower().replace(" ", "_")
        for char in party:
            if char.get("id") == target or char.get("name", "").lower() == character_id_or_name.lower():
                return char
        return None

    def update_character(self, updated_character: Dict[str, Any]) -> bool:
        data = self._load_json(self.party_file)
        party = data.get("party", [])
        char_id = updated_character.get("id")
        
        found = False
        for i, char in enumerate(party):
            if char.get("id") == char_id:
                party[i] = updated_character
                found = True
                break
        
        if not found:
            party.append(updated_character)
            
        data["party"] = party
        self._save_json(self.party_file, data)
        self.sync_character_to_markdown(updated_character)
        return True

    # NPCs
    def get_npcs(self) -> List[Dict[str, Any]]:
        data = self._load_json(self.npcs_file)
        return data.get("npcs", [])

    def get_npc(self, npc_id_or_name: str) -> Optional[Dict[str, Any]]:
        npcs = self.get_npcs()
        target = npc_id_or_name.lower().replace(" ", "_")
        for n in npcs:
            if n.get("id") == target or n.get("name", "").lower() == npc_id_or_name.lower():
                return n
        return None

    def save_npcs(self, npcs_list: List[Dict[str, Any]]) -> None:
        self._save_json(self.npcs_file, {"npcs": npcs_list})

    def update_npc(self, updated_npc: Dict[str, Any]) -> bool:
        data = self._load_json(self.npcs_file)
        npcs = data.get("npcs", [])
        npc_id = updated_npc.get("id")
        
        found = False
        for i, npc in enumerate(npcs):
            if npc.get("id") == npc_id:
                npcs[i] = updated_npc
                found = True
                break
        if not found:
            npcs.append(updated_npc)
            
        data["npcs"] = npcs
        self._save_json(self.npcs_file, data)
        return True

    # Quests
    def get_quests(self) -> Dict[str, Any]:
        return self._load_json(self.quests_file)

    def save_quests(self, quests_data: Dict[str, Any]) -> None:
        self._save_json(self.quests_file, quests_data)

    def update_quests(self, quests_data: Dict[str, Any]) -> bool:
        self._save_json(self.quests_file, quests_data)
        return True

    def get_relationships(self) -> Dict[str, Any]:
        return self._load_json(self.relationships_file)

    def save_relationships(self, relationships_data: Dict[str, Any]) -> None:
        self._save_json(self.relationships_file, relationships_data)

    def update_relationships(self, relationships_data: Dict[str, Any]) -> bool:
        self._save_json(self.relationships_file, relationships_data)
        return True

    # Adventure State Assets
    def get_items(self) -> Dict[str, Any]:
        return self._load_json(self.items_file)

    def get_locations(self) -> Dict[str, Any]:
        return self._load_json(self.locations_file)

    def get_encounters(self) -> List[Dict[str, Any]]:
        data = self._load_json(self.encounters_file)
        return data if isinstance(data, list) else []

    def get_monsters(self) -> Dict[str, Any]:
        return self._load_json(self.monsters_file)

    # Bi-directional Markdown Synchronization
    def sync_character_to_markdown(self, char: Dict[str, Any]):
        """Generates or updates campaign/characters/<char_id>.md from JSON state."""
        char_dir = self.campaign_dir / "characters"
        char_dir.mkdir(parents=True, exist_ok=True)
        md_file = char_dir / f"{char.get('id', 'character')}.md"

        stats = char.get("stats", {})
        skills = char.get("skills", {})
        features = char.get("features", [])
        personality = char.get("personality", {})
        equipment = char.get("equipment", [])

        player_str = f" ({char.get('player_name')})" if char.get("player_name") else ""
        lines = [
            f"# {char.get('name', 'Unknown Hero')}",
            "",
            f"- **Role**: {'Player Character' if char.get('is_player', True) else 'Companion NPC'}{player_str}",
            f"- **Class & Level**: {char.get('class', 'Fighter')} {char.get('level', 1)}",
            f"- **Species**: {char.get('species', 'Human')}",
            f"- **Background**: {char.get('background', 'Soldier')}",
            f"- **Alignment**: {char.get('alignment', 'Neutral')}",
            f"- **Armor Class**: {char.get('ac', 10)}",
            f"- **Speed**: {char.get('speed', 30)} ft",
            f"- **HP:** {char.get('hp', {}).get('current', 10)}/{char.get('hp', {}).get('max', 10)}",
            f"- **Hit Dice**: {char.get('hit_dice', {}).get('current', 1)}/{char.get('hit_dice', {}).get('max', 1)} ({char.get('hit_dice', {}).get('die', '1d10')})",
            f"- **Proficiency Bonus**: +{char.get('proficiency_bonus', 2)}",
        ]

        if char.get("languages"):
            lines.append(f"- **Languages**: {', '.join(char.get('languages', []))}")

        lines.extend([
            "",
            "## Ability Scores",
            "",
            "| Ability | Score | Modifier |",
            "|---|---|---|",
            f"| STR | {stats.get('strength', 10)} | {calculate_modifier(stats.get('strength', 10)):+d} |",
            f"| DEX | {stats.get('dexterity', 10)} | {calculate_modifier(stats.get('dexterity', 10)):+d} |",
            f"| CON | {stats.get('constitution', 10)} | {calculate_modifier(stats.get('constitution', 10)):+d} |",
            f"| INT | {stats.get('intelligence', 10)} | {calculate_modifier(stats.get('intelligence', 10)):+d} |",
            f"| WIS | {stats.get('wisdom', 10)} | {calculate_modifier(stats.get('wisdom', 10)):+d} |",
            f"| CHA | {stats.get('charisma', 10)} | {calculate_modifier(stats.get('charisma', 10)):+d} |",
            "",
            "## Equipment & Coinage",
            f"- **Currency**: {char.get('gold', 0)} GP, {char.get('silver', 0)} SP, {char.get('copper', 0)} CP",
            "",
            "### Inventory",
        ])
        for eq in equipment:
            lines.append(f"- {eq}")

        if "cantrips" in char or "spell_slots" in char or "spells_prepared" in char:
            lines.extend([
                "",
                "## Spellcasting",
            ])
            if "cantrips" in char:
                lines.append(f"- **Cantrips**: {', '.join(char.get('cantrips', []))}")
            if "spells_prepared" in char:
                lines.append(f"- **Spells Prepared**: {', '.join(char.get('spells_prepared', []))}")

        lines.extend([
            "",
            "## Features & Traits",
        ])
        for f in features:
            lines.append(f"- {f}")

        if personality:
            lines.extend([
                "",
                "## Personality & Roleplay",
                f"- **Personality Traits**: {', '.join(personality.get('traits', []))}",
                f"- **Ideals**: {', '.join(personality.get('ideals', []))}",
                f"- **Bonds**: {', '.join(personality.get('bonds', []))}",
                f"- **Flaws**: {', '.join(personality.get('flaws', []))}",
            ])

        with open(md_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
