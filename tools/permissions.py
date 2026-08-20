"""
Security & Permission Engine for Agentic D&D.
Enforces strict sandboxing between Game Mode (player runtime) and Developer Mode (privileged developer runtime).
"""

from enum import Enum
from typing import Set, Optional, Dict, Any


class RuntimeMode(str, Enum):
    GAME_MODE = "GAME_MODE"
    DEVELOPER_MODE = "DEVELOPER_MODE"


class GameModeSecurityViolation(Exception):
    """Raised when an action in Game Mode attempts an unauthorized operation."""
    pass


# Allowlisted operations in Game Mode
GAME_MODE_ALLOWED_OPERATIONS: Set[str] = {
    # Dice & Mechanics
    "dice.roll",
    "dice.parse",
    "mechanics.check",
    "mechanics.saving_throw",
    "mechanics.modifier",
    "mechanics.dc",
    "mechanics.validate_action",
    # Combat
    "combat.initiative",
    "combat.attack",
    "combat.damage",
    "combat.apply_damage",
    "combat.apply_healing",
    "combat.condition_apply",
    "combat.condition_remove",
    "combat.death_save",
    # State Read & Update
    "state.read_world",
    "state.read_party",
    "state.read_npcs",
    "state.read_combat",
    "state.read_quests",
    "state.read_relationships",
    "state.read_campaign_file",
    "state.update_character_hp",
    "state.update_character_resources",
    "state.update_character_inventory",
    "state.update_npc",
    "state.update_world",
    "state.update_quest",
    "state.update_combat",
    # Versioning
    "versioning.commit",
    "versioning.history",
    "versioning.diff",
    # Agents
    "agent.orchestrator",
    "agent.dm",
    "agent.rules",
    "agent.combat",
    "agent.npc",
    "agent.world",
    "agent.character",
    "agent.impact",
}

# Forbidden operations in Game Mode
GAME_MODE_FORBIDDEN_OPERATIONS: Set[str] = {
    "shell.execute",
    "package.install",
    "engine.modify",
    "agent.modify",
    "agent.developer",
    "permission.modify",
    "secret.read",
    "tool.create",
    "file.delete",
    "code.refactor",
}


class PermissionManager:
    """
    Validates and enforces security permissions for tool calls and file operations.
    """

    def __init__(self, default_mode: RuntimeMode = RuntimeMode.GAME_MODE):
        self.current_mode = default_mode

    def set_mode(self, mode: RuntimeMode) -> None:
        self.current_mode = mode

    def is_developer_mode(self) -> bool:
        return self.current_mode == RuntimeMode.DEVELOPER_MODE

    def assert_allowed(self, operation: str) -> None:
        """
        Validates if the requested operation is permitted in the current mode.
        Raises GameModeSecurityViolation if unauthorized.
        """
        if self.current_mode == RuntimeMode.DEVELOPER_MODE:
            # Developer mode has elevated authority
            return

        # Game Mode verification
        clean_op = operation.lower().strip()
        
        if clean_op in GAME_MODE_FORBIDDEN_OPERATIONS or clean_op.startswith("dev.") or clean_op.startswith("developer."):
            raise GameModeSecurityViolation(
                f"Security Violation: Operation '{operation}' is forbidden in Game Mode. "
                f"Requires Developer Mode privileges."
            )

        # Allowlist check
        if clean_op not in GAME_MODE_ALLOWED_OPERATIONS:
            # Check if it starts with an allowed prefix (e.g. dice.*, mechanics.*, etc.)
            prefix = clean_op.split(".")[0] if "." in clean_op else clean_op
            allowed_prefixes = {"dice", "mechanics", "combat", "state", "versioning", "agent"}
            if prefix not in allowed_prefixes:
                raise GameModeSecurityViolation(
                    f"Security Violation: Unauthorized operation '{operation}' in Game Mode."
                )

    def check_file_access(self, file_path: str, is_write: bool = False) -> None:
        """
        Ensures Game Mode can only write to game state and campaign files, never engine code.
        """
        if self.current_mode == RuntimeMode.DEVELOPER_MODE:
            return

        norm_path = file_path.replace("\\", "/").lower()
        if is_write:
            # Game Mode can only write to campaign/ or state/
            if not (norm_path.startswith("campaign/") or norm_path.startswith("state/") or "/campaign/" in norm_path or "/state/" in norm_path):
                raise GameModeSecurityViolation(
                    f"Security Violation: Game Mode cannot modify core file '{file_path}'."
                )
