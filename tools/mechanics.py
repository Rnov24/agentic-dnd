"""
Deterministic Mechanics Engine for D&D 5e (2024 Revision).
Provides pure, verified functions for ability modifiers, DCs, skill checks,
saving throws, proficiency bonuses, and action validation.
"""

from typing import Dict, Any, Optional, List, Tuple
from tools.dice import roll_d20, roll_dice


SKILL_ABILITY_MAP: Dict[str, str] = {
    "athletics": "strength",
    "acrobatics": "dexterity",
    "sleight_of_hand": "dexterity",
    "stealth": "dexterity",
    "arcana": "intelligence",
    "history": "intelligence",
    "investigation": "intelligence",
    "nature": "intelligence",
    "religion": "intelligence",
    "animal_handling": "wisdom",
    "insight": "wisdom",
    "medicine": "wisdom",
    "perception": "wisdom",
    "survival": "wisdom",
    "deception": "charisma",
    "intimidation": "charisma",
    "performance": "charisma",
    "persuasion": "charisma",
}

DC_DIFFICULTY_MAP: Dict[str, int] = {
    "very_easy": 5,
    "easy": 10,
    "medium": 15,
    "hard": 20,
    "very_hard": 25,
    "nearly_impossible": 30,
}


def calculate_modifier(score: int) -> int:
    """Calculates D&D ability score modifier: (score - 10) // 2."""
    return (score - 10) // 2


def calculate_proficiency_bonus(level: int) -> int:
    """Calculates proficiency bonus based on character level (2024 revision)."""
    if level < 1:
        level = 1
    return 2 + ((level - 1) // 4)


def calculate_dc(difficulty: Any) -> int:
    """
    Returns standard DC from difficulty string ('easy', 'medium', 'hard')
    or passes through numeric DC directly.
    """
    if isinstance(difficulty, int):
        return difficulty
    key = str(difficulty).lower().strip().replace(" ", "_").replace("-", "_")
    return DC_DIFFICULTY_MAP.get(key, 15)


def roll_check(
    character: Dict[str, Any],
    ability: Optional[str] = None,
    skill: Optional[str] = None,
    dc: int = 15,
    advantage: bool = False,
    disadvantage: bool = False,
    guidance: bool = False,
    extra_bonus: int = 0,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Performs a deterministic D&D 5e (2024) Ability or Skill Check.
    
    Args:
        character: Character dictionary with stats, skills, level.
        ability: e.g. "strength", "dexterity", "wisdom"
        skill: e.g. "stealth", "perception", "athletics"
        dc: Difficulty Class to beat
        advantage: Roll with advantage
        disadvantage: Roll with disadvantage
        guidance: Add 1d4 guidance bonus
        extra_bonus: Any situational bonus
        seed: Optional RNG seed
        
    Returns:
        Structured check result with full roll and success/failure breakdown.
    """
    stats = character.get("stats", {})
    char_level = character.get("level", 1)
    prof_bonus = calculate_proficiency_bonus(char_level)
    
    # Determine ability from skill if omitted
    clean_skill = skill.lower().replace(" ", "_") if skill else None
    if clean_skill and not ability:
        ability = SKILL_ABILITY_MAP.get(clean_skill, "dexterity")
        
    clean_ability = (ability or "strength").lower().strip()
    ability_score = stats.get(clean_ability, 10)
    ability_mod = calculate_modifier(ability_score)
    
    # Check skill proficiency or expertise
    proficiencies: List[str] = character.get("proficiencies", {}).get("skills", [])
    expertise: List[str] = character.get("proficiencies", {}).get("expertise", [])
    
    skill_mod = 0
    is_proficient = False
    has_expertise = False
    
    if clean_skill:
        if clean_skill in expertise:
            skill_mod = prof_bonus * 2
            has_expertise = True
            is_proficient = True
        elif clean_skill in proficiencies:
            skill_mod = prof_bonus
            is_proficient = True
            
    total_mod = ability_mod + skill_mod + extra_bonus
    
    roll_res = roll_d20(
        modifier=total_mod,
        advantage=advantage,
        disadvantage=disadvantage,
        seed=seed,
    )
    
    guidance_roll = 0
    if guidance:
        g_res = roll_dice("1d4", seed=seed)
        guidance_roll = g_res["total"]
        roll_res["total"] += guidance_roll
        roll_res["formula"] += f" + guidance({guidance_roll}) = {roll_res['total']}"
        
    total = roll_res["total"]
    success = total >= dc
    margin = total - dc

    audit_parts = [
        f"Base d20 Roll: {roll_res['individual_rolls'][0] if roll_res['individual_rolls'] else 0}",
        f"{clean_ability.capitalize()} Modifier: {ability_mod:+d}",
    ]
    if is_proficient:
        audit_parts.append(f"Proficiency Bonus: {skill_mod:+d}" + (" (Expertise)" if has_expertise else ""))
    if extra_bonus:
        audit_parts.append(f"Situational Bonus: {extra_bonus:+d}")
    if guidance_roll:
        audit_parts.append(f"Guidance Bonus (1d4): +{guidance_roll}")
    audit_parts.append(f"Total: {total} vs DC {dc} -> {'SUCCESS' if success else 'FAILURE'} (Margin: {margin:+d})")
    
    return {
        "character_name": character.get("name", "Unknown"),
        "check_type": clean_skill if clean_skill else clean_ability,
        "ability": clean_ability,
        "ability_score": ability_score,
        "ability_modifier": ability_mod,
        "skill": clean_skill,
        "is_proficient": is_proficient,
        "has_expertise": has_expertise,
        "proficiency_bonus": prof_bonus,
        "extra_bonus": extra_bonus,
        "guidance_bonus": guidance_roll,
        "total_modifier": total_mod + guidance_roll,
        "modifier_breakdown": {
            "ability": ability_mod,
            "proficiency": skill_mod,
            "extra": extra_bonus,
            "guidance": guidance_roll
        },
        "dc": dc,
        "natural_roll": roll_res["individual_rolls"][0] if roll_res["individual_rolls"] else 0,
        "total": total,
        "success": success,
        "margin": margin,
        "is_crit_20": roll_res["is_crit_20"],
        "is_crit_1": roll_res["is_crit_1"],
        "advantage_mode": roll_res["advantage_mode"],
        "formula": roll_res["formula"],
        "audit_breakdown": audit_parts,
        "audit_explanation": " | ".join(audit_parts),
    }


def roll_saving_throw(
    character: Dict[str, Any],
    ability: str,
    dc: int = 15,
    advantage: bool = False,
    disadvantage: bool = False,
    extra_bonus: int = 0,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Performs a deterministic D&D 5e Saving Throw with full explainability.
    """
    clean_ability = ability.lower().strip()
    stats = character.get("stats", {})
    ability_score = stats.get(clean_ability, 10)
    ability_mod = calculate_modifier(ability_score)
    char_level = character.get("level", 1)
    prof_bonus = calculate_proficiency_bonus(char_level)
    
    # Check save proficiencies
    save_profs: List[str] = character.get("proficiencies", {}).get("saving_throws", [])
    is_proficient = clean_ability in save_profs
    save_mod = ability_mod + (prof_bonus if is_proficient else 0) + extra_bonus
    
    roll_res = roll_d20(
        modifier=save_mod,
        advantage=advantage,
        disadvantage=disadvantage,
        seed=seed,
    )
    
    total = roll_res["total"]
    success = total >= dc
    margin = total - dc

    audit_parts = [
        f"Base d20 Roll: {roll_res['individual_rolls'][0] if roll_res['individual_rolls'] else 0}",
        f"{clean_ability.capitalize()} Modifier: {ability_mod:+d}",
    ]
    if is_proficient:
        audit_parts.append(f"Save Proficiency: +{prof_bonus}")
    if extra_bonus:
        audit_parts.append(f"Extra Bonus: {extra_bonus:+d}")
    audit_parts.append(f"Total: {total} vs DC {dc} -> {'SUCCESS' if success else 'FAILURE'}")
    
    return {
        "character_name": character.get("name", "Unknown"),
        "ability": clean_ability,
        "ability_modifier": ability_mod,
        "is_proficient": is_proficient,
        "proficiency_bonus": prof_bonus,
        "extra_bonus": extra_bonus,
        "total_modifier": save_mod,
        "dc": dc,
        "natural_roll": roll_res["individual_rolls"][0] if roll_res["individual_rolls"] else 0,
        "total": total,
        "success": success,
        "margin": margin,
        "is_crit_20": roll_res["is_crit_20"],
        "is_crit_1": roll_res["is_crit_1"],
        "advantage_mode": roll_res["advantage_mode"],
        "formula": roll_res["formula"],
        "audit_breakdown": audit_parts,
        "audit_explanation": " | ".join(audit_parts),
    }


def validate_action(
    actor: Dict[str, Any],
    action_name: str,
    resource_cost: Optional[Dict[str, int]] = None,
) -> Tuple[bool, str]:
    """
    Validates if an actor can perform an action according to rules (HP > 0, not incapacitated,
    has necessary spell slots or resources).
    """
    hp = actor.get("hp", {}).get("current", 0)
    if hp <= 0:
        return False, f"{actor.get('name', 'Actor')} is unconscious/incapacitated and cannot act."
        
    conditions = actor.get("conditions", [])
    incapacitating = ["incapacitated", "paralyzed", "petrified", "stunned", "unconscious"]
    for c in conditions:
        if c.lower() in incapacitating:
            return False, f"{actor.get('name', 'Actor')} is {c} and cannot take actions."
            
    if resource_cost:
        resources = actor.get("resources", {})
        for res_key, cost in resource_cost.items():
            current_val = resources.get(res_key, 0)
            if current_val < cost:
                return False, f"Insufficient {res_key}: requires {cost}, has {current_val}."
                
    return True, "Action is valid."
