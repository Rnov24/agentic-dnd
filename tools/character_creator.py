"""
D&D 5e (2024 Revision, Basic Rules, & LMoP) Character Creator Engine.
Handles ability score generation (Standard Array, 4d6-Drop-Lowest, Point Buy),
12 core classes, 15 species/subraces, backgrounds with personality traits,
equipment packs, starting features, and official LMoP starter set presets.

Loads all templates dynamically from rules/*.json via Compendium.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from tools.state_manager import StateManager
from tools.dice import roll_dice
from tools.compendium import Compendium


# Backwards compatibility accessors
def get_class_templates():
    return Compendium.get_instance().get_classes()

def get_species_templates():
    return Compendium.get_instance().get_all_species()

def get_background_templates():
    return Compendium.get_instance().get_all_backgrounds()

def get_presets():
    return Compendium.get_instance().get_all_presets()

CLASS_TEMPLATES = get_class_templates()
SPECIES_TEMPLATES = get_species_templates()
BACKGROUND_TEMPLATES = get_background_templates()
LMOP_PRESETS = get_presets()

# Point buy cost table for ability scores 8 to 15
POINT_BUY_COSTS = {
    8: 0, 9: 1, 10: 2, 11: 3, 12: 4, 13: 5, 14: 7, 15: 9
}


def validate_point_buy(scores: Dict[str, int]) -> Tuple[bool, int, str]:
    """
    Validates whether a set of 6 base ability scores is a valid 27-point point buy.
    """
    stats = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
    total_cost = 0
    for s in stats:
        val = scores.get(s, 8)
        if val < 8 or val > 15:
            return False, total_cost, f"Score for {s.upper()} ({val}) is outside point-buy range [8, 15]."
        total_cost += POINT_BUY_COSTS[val]

    if total_cost > 27:
        return False, total_cost, f"Total point-buy cost ({total_cost}) exceeds 27 point budget."
    return True, total_cost, f"Valid point buy (Cost: {total_cost}/27 points)."


def compute_modifier(score: int) -> int:
    return (score - 10) // 2


def generate_scores(method: str = "standard", seed: Optional[int] = None) -> List[int]:
    """Generates 6 ability scores using standard array or 4d6-drop-lowest."""
    if method == "standard":
        return [15, 14, 13, 12, 10, 8]
    elif method == "roll":
        scores = []
        for _ in range(6):
            rolls = roll_dice("4d6", seed=seed)["individual_rolls"].copy()
            rolls.sort()
            scores.append(sum(rolls[1:]))
        scores.sort(reverse=True)
        return scores
    return [15, 14, 13, 12, 10, 8]


class CharacterCreator:
    def __init__(self, project_root: Optional[str] = None):
        self.sm = StateManager(project_root)
        self.compendium = Compendium.get_instance(project_root)

    def create_character(
        self,
        name: Optional[str] = None,
        char_class: str = "Fighter",
        species: str = "Human",
        background: str = "Soldier",
        method: str = "standard",
        custom_scores: Optional[Dict[str, int]] = None,
        is_player: bool = True,
        preset: Optional[str] = None,
        seed: Optional[int] = None,
        save_to_state: bool = True,
        save_to_vault: bool = True
    ) -> Dict[str, Any]:
        """Creates a fully-calculated D&D 5e (2024) character."""
        if preset:
            p_data = self.compendium.get_preset(preset)
            if p_data:
                name = name or p_data.get("name")
                char_class = p_data.get("class", char_class)
                species = p_data.get("species", species)
                background = p_data.get("background", background)
                custom_scores = p_data.get("scores", {}).copy()

        # Sanitize & resolve inputs via Compendium
        class_data = self.compendium.get_class(char_class)
        if not class_data:
            class_data = self.compendium.get_class("Fighter")
            char_class = "Fighter"
        else:
            for k, v in self.compendium.get_classes().items():
                if v == class_data:
                    char_class = k
                    break

        species_data = self.compendium.get_species(species)
        if not species_data:
            species_data = self.compendium.get_species("Human")
            species = "Human"
        else:
            for k, v in self.compendium.get_all_species().items():
                if v == species_data:
                    species = k
                    break

        bg_data = self.compendium.get_background(background)
        if not bg_data:
            bg_data = self.compendium.get_background("Soldier")
            background = "Soldier"
        else:
            for k, v in self.compendium.get_all_backgrounds().items():
                if v == bg_data:
                    background = k
                    break

        if not name:
            name = f"{species} {char_class}"

        # Assign base ability scores
        if custom_scores and len(custom_scores) == 6:
            base_scores = custom_scores.copy()
            final_scores = custom_scores.copy()
            if species_data.get("bonuses"):
                for stat, bon in species_data.get("bonuses", {}).items():
                    final_scores[stat] = base_scores.get(stat, 10) + bon
        else:
            raw_scores = generate_scores(method, seed=seed)
            primary = class_data.get("primary_ability", ["strength"])
            remaining = [s for s in ["strength", "constitution", "dexterity", "wisdom", "intelligence", "charisma"] if s not in primary]
            stat_order = primary + remaining
            base_scores = {}
            for stat, val in zip(stat_order, raw_scores):
                base_scores[stat] = val

            final_scores = base_scores.copy()
            if species_data.get("bonuses"):
                for stat, bon in species_data.get("bonuses", {}).items():
                    final_scores[stat] = base_scores.get(stat, 10) + bon
            else:
                # Apply 2024 Background ability score bonuses (+2 to primary, +1 to secondary from bg_data)
                bg_scores = bg_data.get("ability_scores", ["strength", "dexterity", "constitution"])
                if len(bg_scores) >= 2:
                    final_scores[bg_scores[0]] = final_scores.get(bg_scores[0], 10) + 2
                    final_scores[bg_scores[1]] = final_scores.get(bg_scores[1], 10) + 1
                elif len(bg_scores) == 1:
                    final_scores[bg_scores[0]] = final_scores.get(bg_scores[0], 10) + 2

        # Calculate HP
        con_mod = compute_modifier(final_scores["constitution"])
        hit_die_str = str(class_data.get("hit_die", "1d8")).replace("1d", "").replace("d", "")
        base_hp = int(hit_die_str) if hit_die_str.isdigit() else 8
        extra_hp = 1 if "Dwarven Toughness" in " ".join(species_data.get("traits", [])) else 0
        if bg_data.get("feat") == "Tough":
            extra_hp += 2
        max_hp = max(1, base_hp + con_mod + extra_hp)

        # Calculate AC
        dex_mod = compute_modifier(final_scores["dexterity"])
        wis_mod = compute_modifier(final_scores["wisdom"])
        base_ac = 10 + dex_mod
        if char_class.lower() == "barbarian":
            base_ac = 10 + dex_mod + con_mod
        elif char_class.lower() == "monk":
            base_ac = 10 + dex_mod + wis_mod
        elif char_class.lower() in ["fighter", "paladin"]:
            base_ac = 16  # Chain mail starting default

        # Skills & proficiencies
        prof_bonus = 2
        skills_dict = {}
        all_skills = [
            "acrobatics", "animal_handling", "arcana", "athletics", "deception",
            "history", "insight", "intimidation", "investigation", "medicine",
            "nature", "perception", "performance", "persuasion", "religion",
            "sleight_of_hand", "stealth", "survival"
        ]
        skill_stat_map = {
            "athletics": "strength",
            "acrobatics": "dexterity", "sleight_of_hand": "dexterity", "stealth": "dexterity",
            "arcana": "intelligence", "history": "intelligence", "investigation": "intelligence", "nature": "intelligence", "religion": "intelligence",
            "animal_handling": "wisdom", "insight": "wisdom", "medicine": "wisdom", "perception": "wisdom", "survival": "wisdom",
            "deception": "charisma", "intimidation": "charisma", "performance": "charisma", "persuasion": "charisma"
        }

        proficient_skills = set(bg_data.get("skill_proficiencies", [])) | set(bg_data.get("skills", []))
        if "Keen Senses" in " ".join(species_data.get("traits", [])):
            proficient_skills.add("perception")
        if species.lower() == "human":
            proficient_skills.add("persuasion")

        for sk in all_skills:
            st = skill_stat_map.get(sk, "strength")
            s_mod = compute_modifier(final_scores[st])
            is_prof = sk in proficient_skills
            skills_dict[sk] = {
                "stat": st,
                "proficient": is_prof,
                "bonus": s_mod + (prof_bonus if is_prof else 0),
                "total": s_mod + (prof_bonus if is_prof else 0)
            }

        # Saving Throws
        saving_throws = {}
        class_saves = class_data.get("saving_throws", ["strength", "dexterity"])
        for st in ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]:
            s_mod = compute_modifier(final_scores[st])
            is_prof = st in class_saves
            saving_throws[st] = {
                "proficient": is_prof,
                "modifier": s_mod + (prof_bonus if is_prof else 0)
            }

        # Features & traits
        all_features = list(class_data.get("features_by_level", {}).get("1", [])) + list(species_data.get("traits", []))
        origin_feat = bg_data.get("feat")
        feats_list = [origin_feat] if origin_feat else []
        if species.lower() == "human":
            feats_list.append("Skilled")

        # Starting Weapon Masteries
        mastery_slots = class_data.get("weapon_mastery_slots", 0)
        weapon_masteries = []
        if mastery_slots > 0:
            default_masteries = {
                "fighter": ["Greatsword (Graze)", "Longbow (Slow)", "Shortsword (Vex)"],
                "barbarian": ["Greataxe (Cleave)", "Handaxe (Vex)"],
                "rogue": ["Dagger (Nick)", "Shortbow (Vex)"],
                "paladin": ["Longsword (Sap)", "Javelin (Slow)"],
                "ranger": ["Longbow (Slow)", "Shortsword (Vex)"]
            }
            weapon_masteries = default_masteries.get(char_class.lower(), ["Shortsword (Vex)"] * mastery_slots)[:mastery_slots]

        # Equipment & Attacks
        equipment = list(bg_data.get("equipment", ["Traveler's Clothes", "Pouch", "10 GP"]))
        attacks = [
            {"name": "Unarmed Strike", "type": "melee", "ability": "strength", "bonus": prof_bonus + compute_modifier(final_scores["strength"]), "damage": f"{1 + compute_modifier(final_scores['strength'])}", "damage_type": "bludgeoning"}
        ]
        if char_class.lower() == "fighter":
            attacks.append({"name": "Greatsword", "type": "melee", "ability": "strength", "bonus": prof_bonus + compute_modifier(final_scores["strength"]), "damage": f"2d6+{compute_modifier(final_scores['strength'])}", "damage_type": "slashing", "mastery": "Graze"})
        elif char_class.lower() == "rogue":
            attacks.append({"name": "Dagger", "type": "melee", "ability": "dexterity", "bonus": prof_bonus + compute_modifier(final_scores["dexterity"]), "damage": f"1d4+{compute_modifier(final_scores['dexterity'])}", "damage_type": "piercing", "mastery": "Nick"})
        elif char_class.lower() == "wizard":
            attacks.append({"name": "Quarterstaff", "type": "melee", "ability": "strength", "bonus": prof_bonus + compute_modifier(final_scores["strength"]), "damage": f"1d6+{compute_modifier(final_scores['strength'])}", "damage_type": "bludgeoning", "mastery": "Topple"})

        # Character ID
        char_id = name.lower().replace(" ", "_").replace("'", "")
        die_display = "1d" + hit_die_str

        # Preset personality overrides
        personality_dict = {
            "traits": bg_data.get("traits", []),
            "ideals": bg_data.get("ideals", []),
            "bonds": bg_data.get("bonds", []),
            "flaws": bg_data.get("flaws", [])
        }
        if preset:
            p_data = self.compendium.get_preset(preset)
            if p_data and "personality" in p_data:
                personality_dict = p_data["personality"].copy()

        character = {
            "id": char_id,
            "name": name,
            "is_player": is_player,
            "class": class_data.get("name", char_class.capitalize()),
            "species": species_data.get("name", species.replace("_", " ").title()),
            "background": bg_data.get("name", background.replace("_", " ").title()),
            "level": 1,
            "proficiency_bonus": prof_bonus,
            "hp": {"current": max_hp, "max": max_hp, "temp": 0},
            "ac": base_ac,
            "speed": species_data.get("speed", 30),
            "hit_dice": {"current": 1, "max": 1, "die": die_display},
            "stats": final_scores,
            "base_scores": base_scores,
            "saving_throws": saving_throws,
            "skills": skills_dict,
            "attacks": attacks,
            "feats": feats_list,
            "weapon_masteries": weapon_masteries,
            "equipment": equipment,
            "inventory": equipment,
            "gold": 15,
            "silver": 0,
            "copper": 0,
            "conditions": [],
            "features": all_features,
            "personality": personality_dict
        }

        # Spellcasting Setup
        if class_data.get("spellcaster") or "spellcasting" in class_data:
            character["spellcasting"] = class_data.get("spellcasting", {"ability": class_data.get("spellcasting_ability", "intelligence")}).copy()
            character["spell_slots"] = self.compendium.get_spell_slots(char_class, 1)
            character["cantrips"] = list(class_data.get("cantrips", ["fire_bolt", "mage_hand"]))
            character["spells_prepared"] = list(class_data.get("spells_prepared", ["magic_missile", "shield"]))

        # Save to state and sync Markdown
        if save_to_state:
            self.sm.update_character(character)

        # Save to Global Character Vault
        if save_to_vault:
            try:
                from tools.vault import CharacterVault
                vault = CharacterVault(str(self.project_root))
                vault.save_character(character)
            except Exception:
                pass

        return character
