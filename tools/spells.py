"""
Comprehensive Spellcasting Engine & Compendium for Agentic D&D.
Implements official 5e PHB spell rules:
- Cantrip scaling (lvl 1/5/11/17)
- Spell slot tracking & deduction
- Upcasting calculations
- Ritual casting (+10 min, 0 slots)
- Concentration management & checks
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from tools.dice import roll_dice
from tools.combat import apply_damage, apply_healing

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SPELLS_FILE = PROJECT_ROOT / "rules" / "spells.json"

DEFAULT_SPELLS = {
    "fire_bolt": {
        "id": "fire_bolt",
        "name": "Fire Bolt",
        "level": 0,
        "school": "Evocation",
        "casting_time": "1 Action",
        "range": "120 ft",
        "components": ["V", "S"],
        "duration": "Instantaneous",
        "concentration": False,
        "ritual": False,
        "type": "ranged_spell_attack",
        "base_damage": "1d10",
        "damage_type": "fire",
        "scaling": "damage increases by 1d10 at 5th level (2d10), 11th level (3d10), and 17th level (4d10)",
        "description": "You hurl a mote of fire at a creature or object within range. Make a ranged spell attack against the target. On a hit, the target takes 1d10 fire damage."
    },
    "ray_of_frost": {
        "id": "ray_of_frost",
        "name": "Ray of Frost",
        "level": 0,
        "school": "Evocation",
        "casting_time": "1 Action",
        "range": "60 ft",
        "components": ["V", "S"],
        "duration": "Instantaneous",
        "concentration": False,
        "ritual": False,
        "type": "ranged_spell_attack",
        "base_damage": "1d8",
        "damage_type": "cold",
        "effect": "Target speed is reduced by 10 feet until the start of your next turn.",
        "description": "A frigid beam of blue-white light streaks toward a creature within range. On a hit, it takes 1d8 cold damage and its speed is reduced by 10 feet."
    },
    "minor_illusion": {
        "id": "minor_illusion",
        "name": "Minor Illusion",
        "level": 0,
        "school": "Illusion",
        "casting_time": "1 Action",
        "range": "30 ft",
        "components": ["S", "M (a bit of fleece)"],
        "duration": "1 Minute",
        "concentration": False,
        "ritual": False,
        "type": "utility",
        "description": "You create a sound or an image of an object within range that lasts for the duration."
    },
    "guidance": {
        "id": "guidance",
        "name": "Guidance",
        "level": 0,
        "school": "Divination",
        "casting_time": "1 Action",
        "range": "Touch",
        "components": ["V", "S"],
        "duration": "Concentration, up to 1 minute",
        "concentration": True,
        "ritual": False,
        "type": "buff",
        "description": "You touch one willing creature. Once before the spell ends, the target can roll a d4 and add the number rolled to one ability check of its choice."
    },
    "cure_wounds": {
        "id": "cure_wounds",
        "name": "Cure Wounds",
        "level": 1,
        "school": "Evocation",
        "casting_time": "1 Action",
        "range": "Touch",
        "components": ["V", "S"],
        "duration": "Instantaneous",
        "concentration": False,
        "ritual": False,
        "type": "healing",
        "base_healing": "1d8",
        "ability_modifier": "spellcasting",
        "upcasting": "healing increases by 1d8 for each slot level above 1st",
        "description": "A creature you touch regains a number of hit points equal to 1d8 + your spellcasting ability modifier."
    },
    "healing_word": {
        "id": "healing_word",
        "name": "Healing Word",
        "level": 1,
        "school": "Evocation",
        "casting_time": "1 Bonus Action",
        "range": "60 ft",
        "components": ["V"],
        "duration": "Instantaneous",
        "concentration": False,
        "ritual": False,
        "type": "healing",
        "base_healing": "1d4",
        "ability_modifier": "spellcasting",
        "upcasting": "healing increases by 1d4 for each slot level above 1st",
        "description": "A creature of your choice that you can see within range regains hit points equal to 1d4 + your spellcasting ability modifier."
    },
    "magic_missile": {
        "id": "magic_missile",
        "name": "Magic Missile",
        "level": 1,
        "school": "Evocation",
        "casting_time": "1 Action",
        "range": "120 ft",
        "components": ["V", "S"],
        "duration": "Instantaneous",
        "concentration": False,
        "ritual": False,
        "type": "auto_hit",
        "darts": 3,
        "dart_damage": "1d4+1",
        "damage_type": "force",
        "upcasting": "creates 1 more dart for each slot level above 1st",
        "description": "You create three glowing darts of magical force. Each dart hits a creature of your choice that you can see within range, dealing 1d4 + 1 force damage."
    },
    "shield": {
        "id": "shield",
        "name": "Shield",
        "level": 1,
        "school": "Abjuration",
        "casting_time": "1 Reaction",
        "range": "Self",
        "components": ["V", "S"],
        "duration": "1 Round",
        "concentration": False,
        "ritual": False,
        "type": "reaction_buff",
        "bonus_ac": 5,
        "description": "An invisible barrier of magical force appears and protects you. Until the start of your next turn, you have a +5 bonus to AC, including against the triggering attack, and you take no damage from magic missile."
    },
    "mage_armor": {
        "id": "mage_armor",
        "name": "Mage Armor",
        "level": 1,
        "school": "Abjuration",
        "casting_time": "1 Action",
        "range": "Touch",
        "components": ["V", "S", "M (a piece of cured leather)"],
        "duration": "8 Hours",
        "concentration": False,
        "ritual": False,
        "type": "buff",
        "base_ac": 13,
        "description": "You touch a willing creature who isn't wearing armor. The target's base AC becomes 13 + its Dexterity modifier."
    },
    "detect_magic": {
        "id": "detect_magic",
        "name": "Detect Magic",
        "level": 1,
        "school": "Divination",
        "casting_time": "1 Action",
        "range": "Self (30 ft)",
        "components": ["V", "S"],
        "duration": "Concentration, up to 10 minutes",
        "concentration": True,
        "ritual": True,
        "type": "utility",
        "description": "For the duration, you sense the presence of magic within 30 feet of you. If you sense magic in this way, you can use your action to see a faint aura around any visible creature or object."
    },
    "burning_hands": {
        "id": "burning_hands",
        "name": "Burning Hands",
        "level": 1,
        "school": "Evocation",
        "casting_time": "1 Action",
        "range": "Self (15-foot cone)",
        "components": ["V", "S"],
        "duration": "Instantaneous",
        "concentration": False,
        "ritual": False,
        "type": "save_aoe",
        "save_ability": "dexterity",
        "base_damage": "3d6",
        "damage_type": "fire",
        "upcasting": "damage increases by 1d6 for each slot level above 1st",
        "description": "As you hold your hands with thumbs touching, a thin sheet of flames shoots forth. Each creature in a 15-foot cone must make a Dexterity save taking 3d6 fire damage on failure, half on success."
    },
    "misty_step": {
        "id": "misty_step",
        "name": "Misty Step",
        "level": 2,
        "school": "Conjuration",
        "casting_time": "1 Bonus Action",
        "range": "Self (30 ft)",
        "components": ["V"],
        "duration": "Instantaneous",
        "concentration": False,
        "ritual": False,
        "type": "teleport",
        "description": "Briefly surrounded by silvery mist, you teleport up to 30 feet to an unoccupied space that you can see."
    },
    "invisibility": {
        "id": "invisibility",
        "name": "Invisibility",
        "level": 2,
        "school": "Illusion",
        "casting_time": "1 Action",
        "range": "Touch",
        "components": ["V", "S", "M (an eyelash encased in gum arabic)"],
        "duration": "Concentration, up to 1 hour",
        "concentration": True,
        "ritual": False,
        "type": "buff",
        "upcasting": "target one additional creature for each slot level above 2nd",
        "description": "A creature you touch becomes invisible until the spell ends. Anything the target is wearing or carrying is invisible as long as it is on the target's person. The spell ends for a target that attacks or casts a spell."
    },
    "fireball": {
        "id": "fireball",
        "name": "Fireball",
        "level": 3,
        "school": "Evocation",
        "casting_time": "1 Action",
        "range": "150 ft (20-foot radius sphere)",
        "components": ["V", "S", "M (a tiny ball of bat guano and sulfur)"],
        "duration": "Instantaneous",
        "concentration": False,
        "ritual": False,
        "type": "save_aoe",
        "save_ability": "dexterity",
        "base_damage": "8d6",
        "damage_type": "fire",
        "upcasting": "damage increases by 1d6 for each slot level above 3rd",
        "description": "A bright streak flashes from your pointing finger to a point you choose within range and then blossoms with a low roar into an explosion of flame. Each creature in a 20-foot-radius sphere must make a Dexterity saving throw, taking 8d6 fire damage on a failed save, or half as much on a successful one."
    },
    "counterspell": {
        "id": "counterspell",
        "name": "Counterspell",
        "level": 3,
        "school": "Abjuration",
        "casting_time": "1 Reaction",
        "range": "60 ft",
        "components": ["S"],
        "duration": "Instantaneous",
        "concentration": False,
        "ritual": False,
        "type": "counter",
        "description": "You attempt to interrupt a creature in the process of casting a spell. If the creature is casting a spell of 3rd level or lower, its spell fails and has no effect. If casting 4th level or higher, make an ability check using your spellcasting ability (DC 10 + spell level)."
    },
    "revivify": {
        "id": "revivify",
        "name": "Revivify",
        "level": 3,
        "school": "Necromancy",
        "casting_time": "1 Action",
        "range": "Touch",
        "components": ["V", "S", "M (diamonds worth 300 gp, consumed)"],
        "duration": "Instantaneous",
        "concentration": False,
        "ritual": False,
        "type": "resurrection",
        "description": "You touch a creature that has died within the last minute. That creature returns to life with 1 hit point. This spell can't return to life a creature that has died of old age, nor can it restore missing body parts."
    }
}


def load_spells() -> Dict[str, Any]:
    if not SPELLS_FILE.exists():
        SPELLS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SPELLS_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_SPELLS, f, indent=2)
        return DEFAULT_SPELLS
    try:
        with open(SPELLS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_SPELLS


def get_spell(name_or_id: str) -> Optional[Dict[str, Any]]:
    spells = load_spells()
    key = name_or_id.lower().strip().replace(" ", "_")
    if key in spells:
        return spells[key]
    for s_id, s in spells.items():
        if s.get("name", "").lower() == name_or_id.lower().strip():
            return s
    return None


def cast_spell(
    caster: Dict[str, Any],
    spell_name: str,
    target: Optional[Dict[str, Any]] = None,
    slot_level: Optional[int] = None,
    is_ritual: bool = False,
    seed: Optional[int] = None
) -> Dict[str, Any]:
    """
    Executes spellcasting mechanics deterministically:
    - Validates spell existence
    - Checks & deducts spell slot (unless cantrip or ritual)
    - Computes damage, healing, or utility
    - Sets concentration if applicable
    """
    spell = get_spell(spell_name)
    if not spell:
        from tools.suggestions import suggest_spell
        known = caster.get("spells_prepared", []) + caster.get("cantrips", [])
        suggs = suggest_spell(spell_name, known_spells=known)
        return {
            "success": False,
            "error": f"Spell '{spell_name}' not found in compendium.",
            "suggestions": suggs,
            "message": f"Spell '{spell_name}' not found. Did you mean: {', '.join(suggs)}?"
        }
        
    base_level = spell.get("level", 0)
    effective_level = slot_level if (slot_level and slot_level >= base_level) else base_level
    
    # Cantrip vs Leveled Spell Slot Check
    slot_expended = False
    if base_level > 0 and not is_ritual:
        slots = caster.get("spell_slots", {})
        lvl_key = f"level_{effective_level}"
        slot_info = slots.get(lvl_key, {"current": 0, "max": 0})
        if slot_info.get("current", 0) <= 0:
            return {
                "success": False,
                "error": f"{caster.get('name')} has no remaining {effective_level}nd/rd/th level spell slots!"
            }
        slot_info["current"] -= 1
        slots[lvl_key] = slot_info
        caster["spell_slots"] = slots
        slot_expended = True
        
    # Determine Spellcasting Ability Mod
    stats = caster.get("stats", {})
    char_class = caster.get("class", "").lower()
    if char_class in ["wizard"]:
        spell_ability = "intelligence"
    elif char_class in ["cleric", "druid", "ranger"]:
        spell_ability = "wisdom"
    else:
        spell_ability = "charisma"
        
    mod = (stats.get(spell_ability, 10) - 10) // 2
    level = caster.get("level", 1)
    prof = 2 + (level - 1) // 4
    spell_attack_bonus = mod + prof
    spell_save_dc = 8 + mod + prof
    
    # Calculate Effects
    result_payload: Dict[str, Any] = {
        "success": True,
        "spell": spell["name"],
        "spell_name": spell["name"],
        "caster": caster.get("name"),
        "level_cast": effective_level,
        "is_ritual": is_ritual,
        "slot_expended": slot_expended,
        "spell_save_dc": spell_save_dc,
        "spell_attack_bonus": spell_attack_bonus,
        "duration": spell.get("duration"),
        "concentration": spell.get("concentration", False)
    }
    
    # Handle Concentration
    if spell.get("concentration"):
        caster["concentration"] = {"spell": spell["name"], "duration": spell["duration"]}
        
    # Handle Healing Spells (e.g. Cure Wounds)
    if spell.get("type") == "healing":
        extra_dice = effective_level - base_level
        # e.g. Cure Wounds 1d8 -> (1 + extra)d8 + mod
        die_base = spell.get("base_healing", "1d8")
        num_dice = 1 + extra_dice
        die_sides = die_base.split("d")[1] if "d" in die_base else "8"
        heal_expr = f"{num_dice}d{die_sides}+{mod}"
        heal_roll = roll_dice(heal_expr, seed=seed)
        result_payload["healing"] = heal_roll["total"]
        result_payload["formula"] = heal_roll["formula"]
        if target and "hp" in target:
            app_res = apply_healing(target, heal_roll["total"])
            result_payload["target_hp_after"] = app_res["hp_after"]
            result_payload["target_name"] = target.get("name")
            
    # Handle Magic Missile
    elif spell.get("id") == "magic_missile" or spell.get("name", "").lower() == "magic missile":
        extra_darts = effective_level - base_level
        total_darts = 3 + extra_darts
        dart_rolls = []
        total_damage = 0
        for i in range(total_darts):
            d_roll = roll_dice("1d4+1", seed=seed)
            dart_rolls.append(d_roll["total"])
            total_damage += d_roll["total"]
        result_payload["darts_count"] = total_darts
        result_payload["dart_damages"] = dart_rolls
        result_payload["total_damage"] = total_damage
        result_payload["damage_type"] = "force"
        if target and "hp" in target:
            app_res = apply_damage(target, total_damage, "force")
            result_payload["target_hp_after"] = app_res["hp_after"]
            result_payload["target_name"] = target.get("name")
            
    # Handle Damaging AOE / Attack
    elif "base_damage" in spell or "damage" in spell:
        base_dmg = spell.get("base_damage") or spell.get("damage") or "1d10"
        if base_level == 0: # Cantrip scaling
            cantrip_dice = 1
            if level >= 17: cantrip_dice = 4
            elif level >= 11: cantrip_dice = 3
            elif level >= 5: cantrip_dice = 2
            die_sides = base_dmg.split("d")[1] if "d" in base_dmg else "10"
            dmg_expr = f"{cantrip_dice}d{die_sides}"
        else: # Upcasting scaling
            extra_dice = effective_level - base_level
            parts = base_dmg.split("d")
            base_count = int(parts[0]) if parts[0].isdigit() else 1
            die_sides = parts[1]
            dmg_expr = f"{base_count + extra_dice}d{die_sides}"
            
        dmg_roll = roll_dice(dmg_expr, seed=seed)
        result_payload["damage"] = dmg_roll["total"]
        result_payload["formula"] = dmg_roll["formula"]
        result_payload["damage_type"] = spell.get("damage_type", "magical")
        if target and "hp" in target:
            app_res = apply_damage(target, dmg_roll["total"], spell.get("damage_type", "magical"))
            result_payload["target_hp_after"] = app_res["hp_after"]
            result_payload["target_name"] = target.get("name")
            
    return result_payload
