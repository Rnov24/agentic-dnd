"""
Encounter Building & Difficulty Calculator for Agentic D&D.
Implements the official D&D Basic Rules / DMG encounter math:
XP Thresholds, Multipliers, Party Size Adjustments, and Adventuring Day Budgets.
Loads tables dynamically from rules/encounters.json via Compendium.
"""

from typing import Dict, Any, List, Optional, Union
from tools.compendium import Compendium

# Module-level accessors for backwards compatibility
def _get_xp_thresholds_table():
    return {int(k): v for k, v in Compendium.get_instance().get_encounter_rules().get("xp_thresholds_by_level", {}).items()}

def _get_adventuring_day_table():
    return {int(k): v for k, v in Compendium.get_instance().get_encounter_rules().get("adventuring_day_xp", {}).items()}

XP_THRESHOLDS_BY_LEVEL = _get_xp_thresholds_table()
ADVENTURING_DAY_XP = _get_adventuring_day_table()
CR_TO_XP = Compendium.get_instance().get_cr_to_xp()
MULTIPLIER_TIERS = Compendium.get_instance().get_multiplier_tiers()
MULTIPLIER_STEPS = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]


def get_monster_count_multiplier(num_monsters: int, party_size: int = 4) -> float:
    """
    Computes the encounter multiplier with party size adjustments.
    """
    if num_monsters <= 0:
        return 1.0
        
    comp = Compendium.get_instance()
    multiplier_tiers = comp.get_multiplier_tiers()
    base_mult = 1.0
    for max_count, mult in multiplier_tiers:
        if num_monsters <= max_count:
            base_mult = mult
            break
            
    idx = MULTIPLIER_STEPS.index(base_mult) if base_mult in MULTIPLIER_STEPS else 1
    
    # Party size adjustments (D&D Basic Rules)
    if party_size < 3:
        idx = min(len(MULTIPLIER_STEPS) - 1, idx + 1)
    elif party_size >= 6:
        idx = max(0, idx - 1)
        
    return MULTIPLIER_STEPS[idx]


def get_xp_by_cr(cr: Union[str, int, float]) -> int:
    """Returns base XP for a given Challenge Rating."""
    comp = Compendium.get_instance()
    cr_map = comp.get_cr_to_xp()
    cr_str = str(cr).strip()
    return cr_map.get(cr_str, 0)


def calculate_encounter_difficulty(
    party_levels: List[int],
    monster_xps: List[int],
    situational_modifier: int = 0
) -> Dict[str, Any]:
    """
    Evaluates encounter difficulty (Trivial, Easy, Medium, Hard, Deadly).
    """
    if not party_levels:
        party_levels = [1]
        
    comp = Compendium.get_instance()
    party_size = len(party_levels)
    num_monsters = len(monster_xps)
    
    # 1. Determine Party Thresholds
    thresholds = {"easy": 0, "medium": 0, "hard": 0, "deadly": 0}
    for lvl in party_levels:
        clamped_lvl = max(1, min(20, lvl))
        lvl_thresholds = comp.get_xp_thresholds(clamped_lvl)
        for key in thresholds:
            thresholds[key] += lvl_thresholds.get(key, 0)
            
    # 2. Total & Adjusted XP
    base_xp = sum(monster_xps)
    multiplier = get_monster_count_multiplier(num_monsters, party_size)
    adjusted_xp = int(base_xp * multiplier)
    
    # 3. Determine Base Difficulty Tier
    if adjusted_xp < thresholds["easy"]:
        difficulty = "Trivial"
    elif adjusted_xp < thresholds["medium"]:
        difficulty = "Easy"
    elif adjusted_xp < thresholds["hard"]:
        difficulty = "Medium"
    elif adjusted_xp < thresholds["deadly"]:
        difficulty = "Hard"
    else:
        difficulty = "Deadly"
        
    # 4. Apply Situational Adjustment
    difficulty_order = ["Trivial", "Easy", "Medium", "Hard", "Deadly"]
    curr_idx = difficulty_order.index(difficulty)
    adjusted_idx = max(0, min(len(difficulty_order) - 1, curr_idx + situational_modifier))
    final_difficulty = difficulty_order[adjusted_idx]
    
    # 5. Adventuring Day Budget
    day_budget = sum(comp.get_adventuring_day_xp(max(1, min(20, lvl))) for lvl in party_levels)
    pct_of_day = round((adjusted_xp / day_budget) * 100, 1) if day_budget > 0 else 0
    
    return {
        "party_size": party_size,
        "party_levels": party_levels,
        "party_thresholds": thresholds,
        "monster_count": num_monsters,
        "base_xp": base_xp,
        "multiplier": multiplier,
        "adjusted_xp": adjusted_xp,
        "difficulty": final_difficulty,
        "raw_difficulty": difficulty,
        "adventuring_day_budget": day_budget,
        "adventuring_day_percent": pct_of_day,
        "situational_modifier": situational_modifier
    }


def get_adventuring_day_budget(party_levels: List[int]) -> int:
    """Returns the total expected daily adjusted XP for a party."""
    comp = Compendium.get_instance()
    return sum(comp.get_adventuring_day_xp(max(1, min(20, lvl))) for lvl in party_levels)


def get_preset_encounter(preset_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves a preset encounter from active adventure or core encounters."""
    comp = Compendium.get_instance()
    encs = comp.get_encounters()
    clean = preset_id.strip().lower().replace(" ", "_")
    for e in encs:
        if e.get("id", "").lower() == clean or e.get("name", "").lower() == preset_id.strip().lower():
            return e
    for e in encs:
        if clean in e.get("id", "").lower() or clean in e.get("name", "").lower():
            return e
    return None


def evaluate_preset_encounter(
    preset_id: str,
    party_levels: Optional[List[int]] = None,
    situational_modifier: int = 0
) -> Dict[str, Any]:
    """Evaluates difficulty and tactical breakdown of a curated adventure preset encounter."""
    preset = get_preset_encounter(preset_id)
    if not preset:
        comp = Compendium.get_instance()
        return {
            "success": False,
            "error": f"Encounter preset '{preset_id}' not found.",
            "available_presets": [e.get("id") for e in comp.get_encounters()]
        }

    comp = Compendium.get_instance()
    monsters_list = preset.get("monsters", [])
    monster_xps = []
    monster_names = []

    for m_id in monsters_list:
        m_stat = comp.get_monster(m_id)
        if m_stat:
            xp = m_stat.get("xp", 50)
            name = m_stat.get("name", m_id)
        else:
            xp = 50
            name = m_id.replace("_", " ").title()
        monster_xps.append(xp)
        monster_names.append(f"{name} ({xp} XP)")

    if party_levels is None:
        from tools.state_manager import StateManager
        sm = StateManager()
        party = sm.get_party()
        party_levels = [p.get("level", 1) for p in party] if party else [1, 1, 1, 1]

    result = calculate_encounter_difficulty(
        party_levels=party_levels,
        monster_xps=monster_xps,
        situational_modifier=situational_modifier
    )
    result["success"] = True
    result["preset_id"] = preset.get("id")
    result["preset_name"] = preset.get("name")
    result["tactics"] = preset.get("tactics", "")
    result["monsters_breakdown"] = monster_names
    return result
