"""
Unit tests for permissions and security sandboxing.
"""

import unittest
from tools.permissions import PermissionManager, RuntimeMode, GameModeSecurityViolation


class TestPermissions(unittest.TestCase):

    def test_game_mode_allowed_operations(self):
        pm = PermissionManager(RuntimeMode.GAME_MODE)
        # Should not raise exception
        pm.assert_allowed("dice.roll")
        pm.assert_allowed("mechanics.check")
        pm.assert_allowed("combat.attack")
        pm.assert_allowed("state.read_world")

    def test_game_mode_forbidden_operations(self):
        pm = PermissionManager(RuntimeMode.GAME_MODE)
        with self.assertRaises(GameModeSecurityViolation):
            pm.assert_allowed("shell.execute")
        with self.assertRaises(GameModeSecurityViolation):
            pm.assert_allowed("engine.modify")
        with self.assertRaises(GameModeSecurityViolation):
            pm.assert_allowed("developer.inspect")

    def test_developer_mode_authority(self):
        pm = PermissionManager(RuntimeMode.DEVELOPER_MODE)
        # Developer mode has elevated authority
        pm.assert_allowed("shell.execute")
        pm.assert_allowed("engine.modify")
        pm.assert_allowed("code.refactor")

    def test_file_access_sandbox(self):
        pm = PermissionManager(RuntimeMode.GAME_MODE)
        # Writing to campaign or state is allowed
        pm.check_file_access("campaign/characters/aria.md", is_write=True)
        pm.check_file_access("state/world.json", is_write=True)

        # Writing to engine/tools is forbidden in Game Mode
        with self.assertRaises(GameModeSecurityViolation):
            pm.check_file_access("tools/dice.py", is_write=True)


if __name__ == "__main__":
    unittest.main()
