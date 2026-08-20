"""
Unit tests for Dynamic Contextual Action Suggester.
"""

import unittest
from tools.action_suggester import ActionSuggester


class TestActionSuggester(unittest.TestCase):
    def setUp(self):
        self.suggester = ActionSuggester()

    def test_combat_suggestions(self):
        actor = {
            "name": "Valen",
            "class": "Fighter",
            "hp": {"current": 12, "max": 12},
            "attacks": [
                {"name": "Greatsword", "bonus": 5, "damage": "2d6+3", "damage_type": "slashing", "mastery": "Graze"}
            ]
        }
        scene = {
            "threats": ["4 Cragmaw Goblins hiding in thickets"],
            "exits": ["Follow goblin trail"]
        }

        suggs = self.suggester.generate_suggestions(actor, scene, in_combat=True)
        self.assertIn("combat", suggs)
        self.assertGreater(len(suggs["combat"]), 0)
        labels = [s["label"] for s in suggs["combat"]]
        self.assertTrue(any("Greatsword" in l for l in labels))

    def test_exploration_suggestions(self):
        actor = {
            "name": "Aria",
            "class": "Rogue",
            "hp": {"current": 10, "max": 10}
        }
        scene = {
            "description": "Two dead horses lie across the muddy road with arrows.",
            "exits": ["North trail", "South road"]
        }

        suggs = self.suggester.generate_suggestions(actor, scene, in_combat=False)
        self.assertIn("exploration", suggs)
        self.assertGreater(len(suggs["exploration"]), 0)
        labels = [s["label"] for s in suggs["exploration"]]
        self.assertTrue(any("Investigate" in l for l in labels))

    def test_render_action_panel(self):
        actor = {"name": "Li Wei", "hp": {"current": 5, "max": 10}}
        scene = {"threats": ["Goblin"], "exits": ["Cave Entrance"]}
        panel = self.suggester.render_action_panel(actor, scene)
        self.assertIn("TACTICAL COMBAT", panel)
        self.assertIn("EXPLORATION", panel)


if __name__ == "__main__":
    unittest.main()
