"""
Deterministic Python tools package for Agentic D&D.
Handles dice rolling, 5e 2024 mechanics, combat calculations, state persistence,
consequential change analysis, git versioning, and permission boundaries.
"""

from tools.dice import roll_dice, parse_dice, roll_d20
from tools.mechanics import (
    calculate_modifier,
    calculate_dc,
    roll_check,
    roll_saving_throw,
    validate_action,
)
from tools.combat import (
    roll_attack,
    roll_damage,
    apply_damage,
    apply_healing,
    roll_initiative,
    apply_condition,
    remove_condition,
)
from tools.state_manager import StateManager
from tools.impact_analyzer import analyze_impact, ImpactLevel, ConsequentialReport
from tools.git_versioning import CampaignGitManager
from tools.permissions import PermissionManager, GameModeSecurityViolation

__all__ = [
    "roll_dice",
    "parse_dice",
    "roll_d20",
    "calculate_modifier",
    "calculate_dc",
    "roll_check",
    "roll_saving_throw",
    "validate_action",
    "roll_attack",
    "roll_damage",
    "apply_damage",
    "apply_healing",
    "roll_initiative",
    "apply_condition",
    "remove_condition",
    "StateManager",
    "analyze_impact",
    "ImpactLevel",
    "ConsequentialReport",
    "CampaignGitManager",
    "PermissionManager",
    "GameModeSecurityViolation",
]
