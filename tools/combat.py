"""
Deterministic Combat Engine for D&D 5e (2024 Revision).
Handles initiative, attack rolls, damage calculations, resistances/vulnerabilities,
healing, conditions, and death saving throws.
"""

from typing import Dict, Any, List, Optional, Tuple
from tools.dice import roll_d20, roll_dice
from tools.mechanics import calculate_modifier, calculate_proficiency_bonus


VALID_CONDITIONS = [
    "blinded", "charmed", "deafened", "frightened", "grappled",
    "incapacitated", "invisible", "paralyzed", "petrified", "poisoned",
    "prone", "restrained", "stunned", "unconscious", "exhaustion"
]


def roll_initiative(
    participants: List[Dict[str, Any]],
    seed: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Rolls initiative for a list of characters/monsters.
    Sorts descending by total roll, with DEX modifier as tiebreaker.
    """
    tracker: List[Dict[str, Any]] = []
    
    for i, p in enumerate(participants):
        name = p.get("name", f"Combatant_{i+1}")
        stats = p.get("stats", {})
        dex = stats.get("dexterity", 10)
        dex_mod = calculate_modifier(dex)
        
        # Check advantage on initiative (e.g. Barbarian Feral Instinct or Alert feat)
        has_adv = p.get("traits", {}).get("advantage_on_initiative", False)
        
        init_res = roll_d20(modifier=dex_mod, advantage=has_adv, seed=seed)
        total = init_res["total"]
        
        tracker.append({
            "id": p.get("id", name.lower().replace(" ", "_")),
            "name": name,
            "is_player": p.get("is_player", False),
            "dex_mod": dex_mod,
            "natural_roll": init_res["individual_rolls"][0] if init_res["individual_rolls"] else 0,
            "initiative": total,
            "hp": p.get("hp", {"current": 10, "max": 10}),
            "ac": p.get("ac", 10),
            "conditions": list(p.get("conditions", [])),
        })
        
    # Sort by initiative descending, then dex_mod descending
    tracker.sort(key=lambda x: (x["initiative"], x["dex_mod"]), reverse=True)
    return tracker


def roll_attack(
    attacker: Dict[str, Any],
    target: Dict[str, Any],
    attack_name: Optional[str] = None,
    advantage: bool = False,
    disadvantage: bool = False,
    cover: str = "none",
    extra_bonus: int = 0,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Performs a deterministic D&D 5e attack roll against target AC with cover adjustments.
    """
    attacker_name = attacker.get("name", "Attacker")
    target_name = target.get("name", "Target")
    base_ac = target.get("ac", 10)
    
    # Calculate cover bonus
    cover_bonus = 0
    if cover == "half":
        cover_bonus = 2
    elif cover in ["three_quarters", "3/4"]:
        cover_bonus = 5
    elif cover == "total":
        return {
            "attacker": attacker_name,
            "target": target_name,
            "attack_name": attack_name or "Basic Attack",
            "target_ac": base_ac,
            "is_hit": False,
            "is_blocked_by_cover": True,
            "formula": "BLOCKED by Total Cover",
            "cover": "total"
        }
    target_ac = base_ac + cover_bonus
    
    # Locate weapon or attack action
    attacks = attacker.get("attacks", [])
    attack_data: Dict[str, Any] = {}
    if attack_name:
        for atk in attacks:
            if atk.get("name", "").lower() == attack_name.lower():
                attack_data = atk
                break
    if not attack_data and attacks:
        attack_data = attacks[0]
        
    # Calculate attack modifier
    char_level = attacker.get("level", 1)
    prof_bonus = calculate_proficiency_bonus(char_level)
    stats = attacker.get("stats", {})
    
    attack_stat = attack_data.get("ability", "strength").lower()
    stat_mod = calculate_modifier(stats.get(attack_stat, 10))
    weapon_bonus = attack_data.get("bonus", 0)
    
    total_atk_mod = stat_mod + prof_bonus + weapon_bonus + extra_bonus
    
    # Check conditions on attacker/target for automatic adv/disadv
    attacker_conds = [c.lower() for c in attacker.get("conditions", [])]
    target_conds = [c.lower() for c in target.get("conditions", [])]
    
    if "prone" in target_conds:
        # Melee has adv, ranged has disadv. Default assume melee if not specified.
        is_ranged = attack_data.get("type", "melee") == "ranged"
        if is_ranged:
            disadvantage = True
        else:
            advantage = True
            
    if "blinded" in attacker_conds or "poisoned" in attacker_conds or "frightened" in attacker_conds:
        disadvantage = True
    if "paralyzed" in target_conds or "stunned" in target_conds or "unconscious" in target_conds:
        advantage = True
        
    roll_res = roll_d20(
        modifier=total_atk_mod,
        advantage=advantage,
        disadvantage=disadvantage,
        seed=seed,
    )
    
    natural_roll = roll_res["individual_rolls"][0] if roll_res["individual_rolls"] else 0
    is_crit_hit = (natural_roll == 20) or roll_res["is_crit_20"]
    is_crit_fumble = (natural_roll == 1) or roll_res["is_crit_1"]
    
    # Nat 20 always hits, Nat 1 always misses
    if is_crit_hit:
        is_hit = True
    elif is_crit_fumble:
        is_hit = False
    else:
        is_hit = roll_res["total"] >= target_ac
        
    return {
        "attacker": attacker_name,
        "target": target_name,
        "attack_name": attack_data.get("name", attack_name or "Basic Attack"),
        "attack_modifier": total_atk_mod,
        "target_ac": target_ac,
        "natural_roll": natural_roll,
        "total": roll_res["total"],
        "is_hit": is_hit,
        "is_critical_hit": is_crit_hit,
        "is_critical_fumble": is_crit_fumble,
        "advantage_mode": roll_res["advantage_mode"],
        "damage_formula": attack_data.get("damage", "1d6"),
        "damage_type": attack_data.get("damage_type", "slashing"),
        "formula": roll_res["formula"],
    }


def roll_damage(
    attacker: Dict[str, Any],
    target: Dict[str, Any],
    damage_formula: str = "1d8",
    damage_type: str = "slashing",
    is_critical: bool = False,
    ability_bonus_key: Optional[str] = "strength",
    extra_bonus: int = 0,
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Rolls deterministic damage and applies damage resistance / vulnerability.
    """
    stats = attacker.get("stats", {})
    stat_mod = calculate_modifier(stats.get(ability_bonus_key.lower(), 10)) if ability_bonus_key else 0
    total_bonus = stat_mod + extra_bonus
    
    # Roll the damage dice (doubling count if critical)
    roll_res = roll_dice(
        expression=damage_formula,
        is_critical=is_critical,
        bonus=total_bonus,
        seed=seed,
    )
    
    raw_damage = max(1, roll_res["total"])  # Min 1 damage
    
    # Check target resistances, vulnerabilities, immunities
    resistances: List[str] = [r.lower() for r in target.get("resistances", [])]
    vulnerabilities: List[str] = [v.lower() for v in target.get("vulnerabilities", [])]
    immunities: List[str] = [i.lower() for i in target.get("immunities", [])]
    
    clean_type = damage_type.lower().strip()
    multiplier_note = "normal"
    final_damage = raw_damage
    
    if clean_type in immunities:
        final_damage = 0
        multiplier_note = "immune (0x)"
    elif clean_type in resistances:
        final_damage = raw_damage // 2
        multiplier_note = "resistant (0.5x)"
    elif clean_type in vulnerabilities:
        final_damage = raw_damage * 2
        multiplier_note = "vulnerable (2x)"
        
    audit_parts = [
        f"Dice ({damage_formula}{' CRIT' if is_critical else ''}): {roll_res['individual_rolls']}",
        f"Stat Mod ({ability_bonus_key}): {stat_mod:+d}",
    ]
    if extra_bonus:
        audit_parts.append(f"Extra Bonus: {extra_bonus:+d}")
    if multiplier_note != "normal":
        audit_parts.append(f"Target Affinity: {multiplier_note}")
    audit_parts.append(f"Final Damage: {final_damage} {clean_type}")

    return {
        "attacker": attacker.get("name", "Attacker"),
        "target": target.get("name", "Target"),
        "damage_formula": damage_formula,
        "damage_type": clean_type,
        "is_critical": is_critical,
        "dice_rolls": roll_res["individual_rolls"],
        "bonus_added": total_bonus,
        "raw_damage": raw_damage,
        "final_damage": final_damage,
        "multiplier_note": multiplier_note,
        "formula": roll_res["formula"],
        "audit_breakdown": audit_parts,
        "audit_explanation": " | ".join(audit_parts),
    }


def apply_damage(
    target: Dict[str, Any],
    damage_amount: int,
    damage_type: str = "slashing",
) -> Dict[str, Any]:
    """
    Applies damage to target HP and Temp HP, checks for unconsciousness or death.
    """
    hp_dict = target.setdefault("hp", {"current": 10, "max": 10, "temp": 0})
    current_hp = hp_dict.get("current", 10)
    max_hp = hp_dict.get("max", 10)
    temp_hp = hp_dict.get("temp", 0)
    
    rem_damage = damage_amount
    absorbed_by_temp = 0
    
    if temp_hp > 0:
        if temp_hp >= rem_damage:
            absorbed_by_temp = rem_damage
            hp_dict["temp"] = temp_hp - rem_damage
            rem_damage = 0
        else:
            absorbed_by_temp = temp_hp
            rem_damage -= temp_hp
            hp_dict["temp"] = 0
            
    hp_before = current_hp
    new_hp = max(0, current_hp - rem_damage)
    hp_dict["current"] = new_hp
    
    is_unconscious = False
    is_dead = False
    excess_damage = (current_hp - damage_amount) if new_hp == 0 else 0
    
    conditions = target.setdefault("conditions", [])
    
    if new_hp == 0:
        if "unconscious" not in conditions:
            conditions.append("unconscious")
            is_unconscious = True
            
        # Instant death check: excess damage >= max_hp
        if abs(excess_damage) >= max_hp:
            is_dead = True
            if "dead" not in conditions:
                conditions.append("dead")
                
    return {
        "target_name": target.get("name", "Target"),
        "damage_applied": damage_amount,
        "damage_type": damage_type,
        "temp_hp_absorbed": absorbed_by_temp,
        "hp_before": hp_before,
        "hp_after": new_hp,
        "max_hp": max_hp,
        "is_unconscious": is_unconscious,
        "is_dead": is_dead,
        "excess_damage": excess_damage,
    }


def apply_healing(
    target: Dict[str, Any],
    heal_amount: int,
) -> Dict[str, Any]:
    """
    Applies healing to a target, capping at max HP and clearing unconsciousness.
    """
    hp_dict = target.setdefault("hp", {"current": 0, "max": 10, "temp": 0})
    current_hp = hp_dict.get("current", 0)
    max_hp = hp_dict.get("max", 10)
    
    hp_before = current_hp
    new_hp = min(max_hp, current_hp + max(0, heal_amount))
    hp_dict["current"] = new_hp
    
    conditions = target.setdefault("conditions", [])
    recovered_from_unconscious = False
    if hp_before == 0 and new_hp > 0:
        if "unconscious" in conditions:
            conditions.remove("unconscious")
            recovered_from_unconscious = True
            
    return {
        "target_name": target.get("name", "Target"),
        "healed": new_hp - hp_before,
        "hp_before": hp_before,
        "hp_after": new_hp,
        "max_hp": max_hp,
        "recovered_from_unconscious": recovered_from_unconscious,
    }


def apply_condition(
    target: Dict[str, Any],
    condition: str,
    duration_rounds: int = 1,
) -> Dict[str, Any]:
    """Applies a condition (e.g. poisoned, prone, frightened)."""
    clean_cond = condition.lower().strip()
    conditions = target.setdefault("conditions", [])
    if clean_cond not in conditions:
        conditions.append(clean_cond)
    return {
        "target_name": target.get("name", "Target"),
        "condition": clean_cond,
        "status": "applied",
        "all_conditions": conditions,
        "duration_rounds": duration_rounds,
    }


def remove_condition(
    target: Dict[str, Any],
    condition: str,
) -> Dict[str, Any]:
    """Removes a condition from a target."""
    clean_cond = condition.lower().strip()
    conditions = target.setdefault("conditions", [])
    if clean_cond in conditions:
        conditions.remove(clean_cond)
        removed = True
    else:
        removed = False
    return {
        "target_name": target.get("name", "Target"),
        "condition": clean_cond,
        "removed": removed,
        "all_conditions": conditions,
    }


def roll_death_save(
    character: Dict[str, Any],
    seed: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Performs a deterministic Death Saving Throw (DC 10).
    Tracks successes and failures.
    """
    death_saves = character.setdefault("death_saves", {"successes": 0, "failures": 0})
    roll_res = roll_d20(seed=seed)
    nat_roll = roll_res["individual_rolls"][0] if roll_res["individual_rolls"] else 10
    
    is_stable = False
    is_dead = False
    regained_hp = False
    
    if nat_roll == 20:
        # Regain 1 HP and become conscious!
        character.setdefault("hp", {})["current"] = 1
        death_saves["successes"] = 0
        death_saves["failures"] = 0
        remove_condition(character, "unconscious")
        regained_hp = True
    elif nat_roll == 1:
        # Counts as 2 failures
        death_saves["failures"] = min(3, death_saves.get("failures", 0) + 2)
    elif nat_roll >= 10:
        death_saves["successes"] = min(3, death_saves.get("successes", 0) + 1)
    else:
        death_saves["failures"] = min(3, death_saves.get("failures", 0) + 1)
        
    if death_saves["successes"] >= 3:
        is_stable = True
        death_saves["successes"] = 0
        death_saves["failures"] = 0
    elif death_saves["failures"] >= 3:
        is_dead = True
        apply_condition(character, "dead")
        
    return {
        "character_name": character.get("name", "Character"),
        "natural_roll": nat_roll,
        "successes": death_saves["successes"],
        "failures": death_saves["failures"],
        "is_stable": is_stable,
        "is_dead": is_dead,
        "regained_hp": regained_hp,
    }
