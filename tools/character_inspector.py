"""
Character Inspection Engine & Visual Sheet Formatter for Agentic D&D.
Generates comprehensive character sheets with health bars, skill lists,
weapon mastery attacks, spell slot pips, and inventory breakdown.
"""

import json
from typing import Dict, Any, Optional
from tools.state_manager import StateManager
from tools.formatting import (
    render_hp_bar, render_slot_pips, box_header, box_section,
    badge, BOLD, RESET, DIM, CYAN, GREEN, YELLOW, BRIGHT_YELLOW, BRIGHT_CYAN
)


def compute_mod(score: int) -> int:
    return (score - 10) // 2


def format_mod(mod: int) -> str:
    return f"+{mod}" if mod >= 0 else f"{mod}"


class CharacterInspector:
    def __init__(self, project_root: Optional[str] = None):
        self.sm = StateManager(project_root)

    def inspect_character(self, character_id_or_name: str) -> Dict[str, Any]:
        """Retrieves and formats character data for display."""
        party = self.sm.get_party()
        char = None
        clean = character_id_or_name.lower().replace(" ", "_")
        for c in party:
            if c.get("id", "").lower() == clean or c.get("name", "").lower() == character_id_or_name.lower():
                char = c
                break

        if not char:
            return {"success": False, "error": f"Character '{character_id_or_name}' not found in party."}

        return {"success": True, "character": char}

    def render_character_sheet(self, character: Dict[str, Any], tab: str = "all") -> str:
        """Renders visual character sheet."""
        name = character.get("name", "Unknown")
        lvl = character.get("level", 1)
        cls_name = character.get("class", "Adventurer")
        species = character.get("species", character.get("race", "Human"))
        bg = character.get("background", "Folk Hero")
        align = character.get("alignment", "Neutral")
        ctrl = "Player Character" if character.get("is_player", True) else "AI Companion"

        player_str = f" | {DIM}Player:{RESET} {character.get('player_name')}" if character.get("player_name") else ""
        lines = []
        lines.append(box_header(f"{name} — Level {lvl} {species} {cls_name}", width=70))
        lines.append(f"  {DIM}Role:{RESET} {ctrl}{player_str} | {DIM}Background:{RESET} {bg} | {DIM}Alignment:{RESET} {align}")

        if character.get("languages"):
            lines.append(f"  {DIM}Languages:{RESET} {', '.join(character.get('languages', []))}")

        # HP & Defense Bar
        hp = character.get("hp", {})
        cur_hp = hp.get("current", 10)
        if cur_hp is None:
            cur_hp = hp.get("max", 10)
        max_hp = hp.get("max", 10)
        tmp_hp = hp.get("temp", 0) or 0
        ac = character.get("ac", 10)
        speed = character.get("speed", 30)
        if isinstance(speed, dict):
            speed = speed.get("walking", 30)
        hd = character.get("hit_dice", {})
        if isinstance(hd, str):
            hd = {"current": lvl, "max": lvl, "die": hd}
        conds = ", ".join(character.get("conditions", [])) if character.get("conditions") else "None"

        senses_str = ""
        if character.get("senses"):
            senses_data = character.get("senses")
            senses_val = ", ".join(f"{k}: {v}" for k, v in senses_data.items()) if isinstance(senses_data, dict) else str(senses_data)
            senses_str = f" | Senses: {BOLD}{senses_val}{RESET}"

        lines.append(box_section("VITALS & DEFENSE", color=BRIGHT_CYAN))
        lines.append(f"  Health:    {render_hp_bar(cur_hp, max_hp, tmp_hp)}")
        lines.append(f"  Armor Class: {BOLD}{ac}{RESET} | Speed: {BOLD}{speed} ft{RESET} | Hit Dice: {BOLD}{hd.get('current', 1)}/{hd.get('max', 1)}{RESET} ({hd.get('die', '1d8')}){senses_str}")
        lines.append(f"  Conditions:  {conds}")

        # Ability Scores
        stats = character.get("stats", {})
        if not stats and "ability_scores" in character:
            stats = {k: v.get("score", 10) for k, v in character.get("ability_scores", {}).items()}
        saves = character.get("saving_throws", [])
        lines.append(box_section("ABILITY SCORES & SAVING THROWS", color=YELLOW))
        
        stat_order = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
        score_strs = []
        for s in stat_order:
            val = stats.get(s, 10)
            mod = compute_mod(val)
            if isinstance(saves, dict):
                is_save = saves.get(s, {}).get("proficient", False) if isinstance(saves.get(s), dict) else (s in saves.get("proficiencies", []))
            elif isinstance(saves, (list, set)):
                is_save = s.lower() in [x.lower() for x in saves]
            else:
                is_save = False
            save_mark = f"{GREEN}[✓]{RESET}" if is_save else f"{DIM}[ ]{RESET}"
            score_strs.append(f"{s[:3].upper()}: {BOLD}{val:2d}{RESET} ({format_mod(mod):>2}) {save_mark}")
        
        lines.append(f"  {' | '.join(score_strs[:3])}")
        lines.append(f"  {' | '.join(score_strs[3:])}")

        # Attacks
        attacks = character.get("attacks", [])
        if attacks:
            lines.append(box_section("WEAPONS & COMBAT ATTACKS", color=GREEN))
            for a in attacks:
                dmg_type = f" {a.get('damage_type')}" if a.get('damage_type') else ""
                prop = f" {DIM}({a.get('property')}){RESET}" if a.get('property') else ""
                rng = f" {DIM}[Range: {a.get('range')}]{RESET}" if a.get('range') else ""
                bonus_str = f"+{a.get('bonus', 0)}" if a.get('bonus', 0) >= 0 else str(a.get('bonus', 0))
                lines.append(f"  * {BOLD}{a.get('name')}{RESET}: {bonus_str} to hit -> {BOLD}{a.get('damage')}{RESET}{dmg_type}{rng}{prop}")

        # Spellcasting
        spell_slots = character.get("spell_slots")
        if spell_slots or "cantrips" in character:
            lines.append(box_section("SPELLCASTING & SPELL SLOTS", color=BRIGHT_CYAN))
            if "cantrips" in character:
                lines.append(f"  Cantrips: {', '.join(character.get('cantrips', []))}")
            if spell_slots:
                slot_strs = []
                for lvl_key, sl in spell_slots.items():
                    lvl_num = lvl_key.split('_')[1]
                    pips = render_slot_pips(sl.get('current', 0), sl.get('max', 0))
                    slot_strs.append(f"Level {lvl_num}: {pips}")
                lines.append(f"  Spell Slots: {' | '.join(slot_strs)}")
            if "spells_prepared" in character:
                lines.append(f"  Prepared: {', '.join(character.get('spells_prepared', []))}")

        # Inventory & Currency
        inv = character.get("inventory", character.get("equipment", []))
        curr = character.get("currency", {})
        if not curr:
            curr = {"gp": character.get("gold", 0), "sp": character.get("silver", 0), "cp": character.get("copper", 0)}
        lines.append(box_section("INVENTORY & COINAGE", color=YELLOW))
        curr_str = f"{BRIGHT_YELLOW}{curr.get('gp', 0)} GP{RESET}, {curr.get('sp', 0)} SP, {curr.get('cp', 0)} CP"
        lines.append(f"  Currency:  {curr_str}")
        lines.append(f"  Equipment: {', '.join(inv) if inv else 'None'}")

        # Features & Traits
        feats = character.get("features", [])
        if feats:
            lines.append(box_section("FEATURES & SPECIAL TRAITS", color=BRIGHT_YELLOW))
            for f in feats:
                lines.append(f"  • {f}")

        lines.append("\n" + "=" * 70 + "\n")
        return "\n".join(lines)
