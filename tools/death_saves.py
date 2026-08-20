"""
Death Saving Throw & 0 HP Mechanics for Agentic D&D.
Implements 5e PHB rules for unconsciousness at 0 HP, death saves,
instant death from massive damage, and stabilization.
"""

from typing import Dict, Any, Optional
from tools.dice import roll_dice
from tools.mechanics import roll_check


def roll_death_save(character: Dict[str, Any], seed: Optional[int] = None) -> Dict[str, Any]:
    """
    Rolls a death saving throw (1d20 without modifiers) for a character at 0 HP:
    - 20: Critical success -> Regains 1 HP and wakes up!
    - 10-19: 1 Success (3 successes = Stabilized)
    - 2-9: 1 Failure (3 failures = Dead)
    - 1: Critical failure -> 2 Failures!
    """
    hp = character.get("hp", {})
    if hp.get("current", 0) > 0:
        return {
            "success": False,
            "error": f"{character.get('name')} is not at 0 HP (current HP: {hp.get('current')})."
        }
        
    ds = character.get("death_saves", {"successes": 0, "failures": 0, "stabilized": False})
    if ds.get("stabilized"):
        return {
            "success": True,
            "status": "Stabilized",
            "message": f"{character.get('name')} is stabilized and does not need to roll death saves."
        }
        
    roll_res = roll_dice("1d20", seed=seed)
    d20 = roll_res["total"]
    
    result_type = ""
    status = "Dying"
    hp_regained = 0
    
    if d20 == 20:
        result_type = "Critical Success (Natural 20)"
        hp["current"] = 1
        character["hp"] = hp
        # Remove unconscious condition and reset death saves
        conds = [c for c in character.get("conditions", []) if c != "unconscious"]
        character["conditions"] = conds
        character.pop("death_saves", None)
        status = "Revived (1 HP)"
        hp_regained = 1
    elif d20 == 1:
        result_type = "Critical Failure (Natural 1)"
        ds["failures"] = ds.get("failures", 0) + 2
    elif d20 >= 10:
        result_type = "Success"
        ds["successes"] = ds.get("successes", 0) + 1
    else:
        result_type = "Failure"
        ds["failures"] = ds.get("failures", 0) + 1
        
    if d20 != 20:
        if ds["successes"] >= 3:
            ds["stabilized"] = True
            status = "Stabilized"
        elif ds["failures"] >= 3:
            status = "Dead"
            character["status"] = "Dead"
            if "dead" not in character.get("conditions", []):
                character.setdefault("conditions", []).append("dead")
        character["death_saves"] = ds
        
    return {
        "character": character.get("name"),
        "roll": d20,
        "result_type": result_type,
        "successes": ds.get("successes", 0),
        "failures": ds.get("failures", 0),
        "stabilized": ds.get("stabilized", False),
        "status": status,
        "hp_regained": hp_regained,
        "current_hp": character.get("hp", {}).get("current", 0)
    }


def apply_damage_at_zero_hp(
    character: Dict[str, Any],
    damage: int,
    is_critical: bool = False
) -> Dict[str, Any]:
    """
    Applies damage taken while at 0 HP:
    - If damage >= max HP -> Instant Death!
    - Otherwise +1 failure (or +2 failures if critical hit).
    """
    hp = character.get("hp", {})
    max_hp = hp.get("max", 10)
    
    if damage >= max_hp:
        character["status"] = "Dead"
        character["conditions"] = list(set(character.get("conditions", []) + ["dead"]))
        return {
            "character": character.get("name"),
            "instant_death": True,
            "status": "Dead (Massive Damage)",
            "message": f"{character.get('name')} took {damage} damage at 0 HP (>= max HP {max_hp}) and dies instantly!"
        }
        
    ds = character.get("death_saves", {"successes": 0, "failures": 0, "stabilized": False})
    ds["stabilized"] = False
    added_failures = 2 if is_critical else 1
    ds["failures"] = ds.get("failures", 0) + added_failures
    
    status = "Dying"
    if ds["failures"] >= 3:
        status = "Dead"
        character["status"] = "Dead"
        character["conditions"] = list(set(character.get("conditions", []) + ["dead"]))
        
    character["death_saves"] = ds
    return {
        "character": character.get("name"),
        "instant_death": False,
        "damage_taken": damage,
        "failures_added": added_failures,
        "total_failures": ds["failures"],
        "status": status
    }


def stabilize_character(
    healer: Dict[str, Any],
    target: Dict[str, Any],
    seed: Optional[int] = None
) -> Dict[str, Any]:
    """
    Attempts to stabilize an unconscious creature at 0 HP using a DC 10 Wisdom (Medicine) check.
    """
    chk = roll_check(healer, skill="medicine", dc=10, seed=seed)
    if chk["success"]:
        ds = target.get("death_saves", {"successes": 0, "failures": 0})
        ds["stabilized"] = True
        target["death_saves"] = ds
        return {
            "success": True,
            "healer": healer.get("name"),
            "target": target.get("name"),
            "check": chk,
            "message": f"{healer.get('name')} successfully stabilizes {target.get('name')}!"
        }
    else:
        return {
            "success": False,
            "healer": healer.get("name"),
            "target": target.get("name"),
            "check": chk,
            "message": f"{healer.get('name')} fails the Medicine check to stabilize {target.get('name')}."
        }
