"""
Unit tests for Developer Agent and Developer Mode operations.
"""

import unittest
from agents.developer import DeveloperAgent
from tools.permissions import PermissionManager, RuntimeMode, GameModeSecurityViolation


class TestDeveloperMode(unittest.TestCase):

    def test_inspect_repository_in_developer_mode(self):
        dev = DeveloperAgent()
        info = dev.inspect_repository()
        self.assertIn("structure", info)
        self.assertGreater(info["total_directories"], 0)

    def test_run_tests_via_developer_agent(self):
        dev = DeveloperAgent()
        res = dev.run_tests(pattern="test_dice.py")
        self.assertTrue(res["passed"])
        self.assertEqual(res["exit_code"], 0)

    def test_security_violation_in_game_mode(self):
        pm = PermissionManager(RuntimeMode.GAME_MODE)
        dev = DeveloperAgent(permission_manager=pm)
        with self.assertRaises(GameModeSecurityViolation):
            dev.inspect_repository()

    def test_path_traversal_prevention(self):
        dev = DeveloperAgent()
        with self.assertRaises(ValueError):
            dev.read_file("../../outside.txt")
        with self.assertRaises(ValueError):
            dev.write_file("../../outside.txt", "exploit")


if __name__ == "__main__":
    unittest.main()
