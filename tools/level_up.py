"""
D&D 5e Level-Up Progression Engine for Agentic D&D.
Handles HP calculation, proficiency progression, spell slot scaling,
and milestone class features from Level 1 to 20.
Loads progression matrices dynamically from rules/progression.json via Compendium.
"""

from typing import Dict, Any, Optional, List, Tuple
from tools.state_manager import StateManager
from tools.dice import roll_dice
from tools.compendium import Compendium


def get_proficiency_bonus(level: int) -> int:
    return Compendium.get_instance().get_proficiency_bonus(level)


class LevelUpManager:
    def __init__(self, project_root: Optional[str] = None):
        self.sm = StateManager(project_root)
        self.compendium = Compendium.get_instance(project_root)

    def level_up_character(
        self,
        character_id_or_name: str,
        hp_choice: str = "average",
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """Levels up a character from level L to L+1."""
        char = self.sm.get_character(character_id_or_name)
        if not char:
            return {"success": False, "error": f"Character '{character_id_or_name}' not found."}

        cur_level = char.get("level", 1)
        if cur_level >= 20:
            return {"success": False, "error": "Character is already at maximum level 20."}

        new_level = cur_level + 1
        char_class = char.get("class", "Fighter").capitalize()
        hd_info = char.get("hit_dice", {"die": "1d10"})
        die_str = str(hd_info.get("die", "1d10")).replace("1d", "").replace("d", "")
        die_faces = int(die_str) if die_str.isdigit() else 10

        # Calculate HP increase
        con = char.get("stats", {}).get("constitution", 10)
        con_mod = (con - 10) // 2
        extra_hp = 1 if "Dwarven Toughness" in " ".join(char.get("features", [])) else 0

        if hp_choice == "roll":
            roll_res = roll_dice(f"1d{die_faces}", seed=seed)
            hp_gain = max(1, roll_res["total"] + con_mod + extra_hp)
        else:
            avg_die = (die_faces // 2) + 1
            hp_gain = max(1, avg_die + con_mod + extra_hp)

        # Apply HP & Level updates
        char["level"] = new_level
        old_max_hp = char.get("hp", {}).get("max", 10)
        new_max_hp = old_max_hp + hp_gain
        char["hp"]["max"] = new_max_hp
        char["hp"]["current"] = char["hp"].get("current", old_max_hp) + hp_gain
        
        # Hit dice update
        char["hit_dice"]["max"] = new_level
        char["hit_dice"]["current"] = char["hit_dice"].get("current", 1) + 1

        # Proficiency bonus update
        old_prof = char.get("proficiency_bonus", 2)
        new_prof = self.compendium.get_proficiency_bonus(new_level)
        char["proficiency_bonus"] = new_prof
        prof_diff = new_prof - old_prof

        # Recalculate proficient skills
        if prof_diff != 0 and "skills" in char:
            for sk_name, sk_data in char["skills"].items():
                if sk_data.get("proficient"):
                    sk_data["total"] += prof_diff

        # Spell Slots Scaling via Compendium
        new_slots = self.compendium.get_spell_slots(char_class, new_level)
        if new_slots:
            char["spell_slots"] = new_slots
            if "spellcasting" not in char and char_class in ["Paladin", "Ranger"]:
                char["spellcasting"] = {"ability": "charisma" if char_class == "Paladin" else "wisdom"}
            if "spellcasting" in char:
                char["spellcasting"]["spell_slots"] = new_slots

        # New Class Features via Compendium
        new_features = self.compendium.get_class_features_for_level(char_class, new_level)
        for feat in new_features:
            if feat not in char.get("features", []):
                char.setdefault("features", []).append(feat)

        # Save back to state and sync Markdown
        self.sm.update_character(char)

        return {
            "success": True,
            "character": char,
            "old_level": cur_level,
            "new_level": new_level,
            "hp_gain": hp_gain,
            "new_max_hp": new_max_hp,
            "new_features": new_features
        }
