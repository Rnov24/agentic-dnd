"""
Deterministic Dice Roller for Agentic D&D.
Handles standard tabletop dice expressions, advantage/disadvantage, critical hits,
and returns rich structured results for agent verification and transparency.
"""

import random
import re
from typing import Dict, Any, List, Optional, Tuple


def parse_dice(expression: str) -> Tuple[int, int, int]:
    """
    Parses a dice expression like '1d20+5', '2d6', '3d8-2', or '14'.
    Returns: (count, sides, modifier)
    """
    expr = expression.strip().replace(" ", "").lower()
    
    # Handle pure constant like '5' or '+3'
    if re.fullmatch(r"^[+-]?\d+$", expr):
        return (0, 0, int(expr))
    
    # Standard format: {count}d{sides}{+/- modifier}
    pattern = r"^(\d*)d(\d+)([+-]\d+)?$"
    match = re.match(pattern, expr)
    if not match:
        raise ValueError(f"Invalid dice expression: '{expression}'")
    
    count_str, sides_str, mod_str = match.groups()
    count = int(count_str) if count_str else 1
    sides = int(sides_str)
    modifier = int(mod_str) if mod_str else 0
    
    if sides <= 0 or count < 0:
        raise ValueError(f"Dice count and sides must be positive: '{expression}'")
        
    return (count, sides, modifier)


def roll_dice(
    expression: str = "1d20",
    advantage: bool = False,
    disadvantage: bool = False,
    is_critical: bool = False,
    bonus: int = 0,
    seed: Optional[int] = None
) -> Dict[str, Any]:
    """
    Rolls dice based on an expression with deterministic calculation.
    
    Args:
        expression: e.g. "1d20+5", "2d6+3", "1d8"
        advantage: If True and rolling 1d20, rolls 2d20 and takes higher.
        disadvantage: If True and rolling 1d20, rolls 2d20 and takes lower.
        is_critical: If True (e.g. for damage), doubles the number of dice.
        bonus: Additional integer bonus to add to the result.
        seed: Optional RNG seed for repeatable testing.
        
    Returns:
        Structured dictionary with individual rolls, modifiers, total, crit flags.
    """
    rng = random.Random(seed) if seed is not None else random.Random()
    count, sides, expr_modifier = parse_dice(expression)
    total_modifier = expr_modifier + bonus
    
    # Critical hits double dice count for damage rolls (when count > 0)
    if is_critical and count > 0:
        count *= 2
        
    individual_rolls: List[int] = []
    dropped_rolls: List[int] = []
    advantage_mode: str = "NORMAL"
    
    if (advantage or disadvantage) and count == 1 and sides == 20:
        r1 = rng.randint(1, 20)
        r2 = rng.randint(1, 20)
        if advantage and not disadvantage:
            advantage_mode = "ADVANTAGE"
            chosen = max(r1, r2)
            dropped = min(r1, r2)
            individual_rolls = [chosen]
            dropped_rolls = [dropped]
        elif disadvantage and not advantage:
            advantage_mode = "DISADVANTAGE"
            chosen = min(r1, r2)
            dropped = max(r1, r2)
            individual_rolls = [chosen]
            dropped_rolls = [dropped]
        else:
            advantage_mode = "CANCELLED"  # Adv + Disadv cancel out
            individual_rolls = [r1]
            dropped_rolls = []
    else:
        for _ in range(count):
            individual_rolls.append(rng.randint(1, sides))
            
    dice_sum = sum(individual_rolls)
    total = dice_sum + total_modifier
    
    # Check natural 20 or natural 1 for single d20 rolls
    is_crit_20 = (sides == 20 and count == 1 and individual_rolls == [20])
    is_crit_1 = (sides == 20 and count == 1 and individual_rolls == [1])
    
    formatted_rolls = "+".join(map(str, individual_rolls)) if individual_rolls else "0"
    mod_str = f" + {total_modifier}" if total_modifier > 0 else (f" - {abs(total_modifier)}" if total_modifier < 0 else "")
    formula_str = f"[{formatted_rolls}]{mod_str} = {total}"
    
    return {
        "expression": expression,
        "count": count,
        "sides": sides,
        "individual_rolls": individual_rolls,
        "dropped_rolls": dropped_rolls,
        "dice_sum": dice_sum,
        "modifier": total_modifier,
        "total": total,
        "is_crit_20": is_crit_20,
        "is_crit_1": is_crit_1,
        "is_critical": is_critical,
        "advantage_mode": advantage_mode,
        "formula": formula_str,
    }


def roll_d20(
    modifier: int = 0,
    advantage: bool = False,
    disadvantage: bool = False,
    seed: Optional[int] = None
) -> Dict[str, Any]:
    """Helper shortcut for rolling a standard d20 check or save."""
    return roll_dice(
        expression=f"1d20{'+' if modifier >= 0 else ''}{modifier}",
        advantage=advantage,
        disadvantage=disadvantage,
        seed=seed
    )
