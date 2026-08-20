"""
Unit tests for consequential change impact analysis.
"""

import unittest
from tools.impact_analyzer import analyze_impact, ImpactLevel


class TestImpactAnalyzer(unittest.TestCase):

    def test_routine_action_low_impact(self):
        before = {
            "party": [{"id": "aria", "name": "Aria", "hp": {"current": 20, "max": 20}, "conditions": []}],
            "npcs": [{"id": "guard_karl", "name": "Guard Karl", "status": "Alive", "hp": {"current": 16, "max": 16}}],
            "quests": [{"id": "escape", "status": "Active"}]
        }
        after = {
            "party": [{"id": "aria", "name": "Aria", "hp": {"current": 18, "max": 20}, "conditions": []}],
            "npcs": [{"id": "guard_karl", "name": "Guard Karl", "status": "Alive", "hp": {"current": 16, "max": 16}}],
            "quests": [{"id": "escape", "status": "Active"}]
        }
        report = analyze_impact(before, after)
        self.assertFalse(report.is_consequential)
        self.assertEqual(report.impact_level, ImpactLevel.LOW)
        self.assertFalse(report.requires_approval)

    def test_major_npc_death_high_impact(self):
        before = {
            "party": [{"id": "aria", "name": "Aria", "hp": {"current": 20, "max": 20}, "conditions": []}],
            "npcs": [{"id": "captain_aldric", "name": "Captain Aldric", "status": "Alive", "hp": {"current": 50, "max": 50}}],
            "quests": []
        }
        after = {
            "party": [{"id": "aria", "name": "Aria", "hp": {"current": 20, "max": 20}, "conditions": []}],
            "npcs": [{"id": "captain_aldric", "name": "Captain Aldric", "status": "Dead", "hp": {"current": 0, "max": 50}}],
            "quests": []
        }
        report = analyze_impact(before, after, cause="Player defeated Captain Aldric")
        self.assertTrue(report.is_consequential)
        self.assertEqual(report.impact_level, ImpactLevel.HIGH)
        self.assertTrue(report.requires_approval)
        self.assertIn("campaign/npcs/captain_aldric.md", report.affected_files)

    def test_player_character_death_high_impact(self):
        before = {
            "party": [{"id": "aria", "name": "Aria", "hp": {"current": 10, "max": 20}, "conditions": []}],
            "npcs": [],
            "quests": []
        }
        after = {
            "party": [{"id": "aria", "name": "Aria", "hp": {"current": 0, "max": 20}, "conditions": ["dead"]}],
            "npcs": [],
            "quests": []
        }
        report = analyze_impact(before, after)
        self.assertTrue(report.is_consequential)
        self.assertTrue(report.requires_approval)


if __name__ == "__main__":
    unittest.main()
