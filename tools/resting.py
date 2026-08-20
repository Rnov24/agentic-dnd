"""
Resting & Recovery Engine for Agentic D&D.
Implements official 5e PHB rules for Short Rest (Hit Dice healing)
and Long Rest (HP reset, Hit Dice recovery, spell slots restoration, exhaustion reduction).
"""

from typing import Dict, Any, List, Optional
from tools.dice import roll_dice
from tools.state_manager import StateManager


def execute_short_rest(
    character: Dict[str, Any],
    hit_dice_to_spend: int = 1,
    seed: Optional[int] = None
) -> Dict[str, Any]:
    """
    Executes a Short Rest for a character:
    - Spends up to hit_dice_to_spend from remaining Hit Dice
    - Rolls each Hit Die (e.g. 1d8, 1d6) + CON modifier
    - Adds regained HP to current HP up to max HP
    - Resets short-rest features (e.g. second wind)
    """
    char_class = character.get("class", "").lower()
    level = character.get("level", 1)
    
    # Hit Die size by class
    hit_die_map = {
        "wizard": "1d6", "sorcerer": "1d6",
        "rogue": "1d8", "cleric": "1d8", "druid": "1d8", "monk": "1d8", "bard": "1d8", "warlock": "1d8",
        "fighter": "1d10", "paladin": "1d10", "ranger": "1d10",
        "barbarian": "1d12"
    }
    die_type = hit_die_map.get(char_class, "1d8")
    
    # Hit dice tracking
    hit_dice_info = character.get("hit_dice", {"current": level, "max": level, "die": die_type})
    current_hd = hit_dice_info.get("current", level)
    
    if current_hd <= 0:
        return {
            "success": False,
            "character": character.get("name"),
            "error": "No remaining Hit Dice to spend during short rest.",
            "hp": character.get("hp", {})
        }
        
    actual_spent = min(hit_dice_to_spend, current_hd)
    con_score = character.get("stats", {}).get("constitution", 10)
    con_mod = (con_score - 10) // 2
    
    total_healed = 0
    rolls_details = []
    
    for i in range(actual_spent):
        roll_res = roll_dice(die_type, bonus=con_mod, seed=seed)
        heal_val = max(1, roll_res["total"])
        total_healed += heal_val
        rolls_details.append({"die": die_type, "con_mod": con_mod, "total": heal_val, "formula": roll_res["formula"]})
        
    # Update HP
    hp = character.get("hp", {"current": 10, "max": 10, "temp": 0})
    hp_before = hp.get("current", 10)
    max_hp = hp.get("max", 10)
    hp_after = min(max_hp, hp_before + total_healed)
    hp["current"] = hp_after
    
    # Update Hit Dice
    hit_dice_info["current"] = current_hd - actual_spent
    character["hit_dice"] = hit_dice_info
    character["hp"] = hp
    
    # Reset short-rest abilities
    if "features" in character and isinstance(character["features"], list):
        for feat in character["features"]:
            if isinstance(feat, dict) and feat.get("recharge") == "short_rest":
                feat["expended"] = False
                
    return {
        "success": True,
        "character": character.get("name"),
        "rest_type": "short_rest",
        "hit_dice_spent": actual_spent,
        "hit_dice_remaining": hit_dice_info["current"],
        "rolls": rolls_details,
        "hp_before": hp_before,
        "hp_healed": hp_after - hp_before,
        "hp_after": hp_after,
        "max_hp": max_hp
    }


def execute_long_rest(character: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes a Long Rest for a character:
    - Restores HP to max
    - Regains spent Hit Dice up to half total Hit Dice (minimum 1)
    - Restores all spell slots (1st-9th)
    - Reduces Exhaustion level by 1
    - Clears temporary conditions (e.g. unconscious if stabilized, frightened)
    """
    hp = character.get("hp", {"current": 10, "max": 10, "temp": 0})
    hp_before = hp.get("current", 10)
    max_hp = hp.get("max", 10)
    hp["current"] = max_hp
    hp["temp"] = 0
    character["hp"] = hp
    
    # Regain Hit Dice: max(1, total_hd // 2)
    level = character.get("level", 1)
    hd_info = character.get("hit_dice", {"current": level, "max": level, "die": "1d8"})
    max_hd = hd_info.get("max", level)
    curr_hd = hd_info.get("current", 0)
    hd_to_recover = max(1, max_hd // 2)
    new_hd = min(max_hd, curr_hd + hd_to_recover)
    hd_recovered = new_hd - curr_hd
    hd_info["current"] = new_hd
    character["hit_dice"] = hd_info
    
    # Restore Spell Slots
    slots_restored = False
    if "spell_slots" in character:
        for lvl_str, slot_data in character["spell_slots"].items():
            if isinstance(slot_data, dict):
                slot_data["current"] = slot_data.get("max", slot_data.get("current", 0))
                slots_restored = True
                
    # Reduce Exhaustion by 1
    conds = character.get("conditions", [])
    exhaustion_reduced = False
    new_conds = []
    for c in conds:
        if c.startswith("exhaustion"):
            parts = c.split("_")
            curr_lvl = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 1
            if curr_lvl > 1:
                new_conds.append(f"exhaustion_{curr_lvl - 1}")
            exhaustion_reduced = True
        elif c in ["unconscious", "frightened", "poisoned"]:
            continue # cleared after long rest
        else:
            new_conds.append(c)
    character["conditions"] = new_conds
    
    # Reset death saves if present
    character.pop("death_saves", None)
    
    return {
        "success": True,
        "character": character.get("name"),
        "rest_type": "long_rest",
        "hp_before": hp_before,
        "hp_after": max_hp,
        "hit_dice_recovered": hd_recovered,
        "hit_dice_current": new_hd,
        "hit_dice_max": max_hd,
        "spell_slots_restored": slots_restored,
        "exhaustion_reduced": exhaustion_reduced,
        "conditions": new_conds
    }
