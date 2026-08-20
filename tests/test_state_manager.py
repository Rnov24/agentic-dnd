"""
Unit tests for state manager and markdown synchronization.
"""

import unittest
import shutil
import tempfile
from pathlib import Path
from tools.state_manager import StateManager


class TestStateManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.sm = StateManager(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_save_and_load_party(self):
        party = [
            {
                "id": "hero_1",
                "name": "Sir Galahad",
                "class": "Paladin",
                "level": 3,
                "hp": {"current": 28, "max": 28, "temp": 0},
                "stats": {"strength": 16, "dexterity": 10, "constitution": 14, "intelligence": 10, "wisdom": 12, "charisma": 15},
                "is_player": True
            }
        ]
        self.sm.save_party(party)
        loaded = self.sm.get_party()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["name"], "Sir Galahad")

        # Verify markdown file was generated
        char_md = Path(self.temp_dir) / "campaign" / "characters" / "hero_1.md"
        self.assertTrue(char_md.exists())
        with open(char_md, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("# Sir Galahad", content)
            self.assertIn("Paladin", content)
            self.assertIn("HP:** 28/28", content)

    def test_update_character_mutation(self):
        party = [{"id": "aria", "name": "Aria", "hp": {"current": 20, "max": 20}}]
        self.sm.save_party(party)

        updated_aria = {"id": "aria", "name": "Aria", "hp": {"current": 12, "max": 20}}
        self.sm.update_character(updated_aria)

        char = self.sm.get_character("aria")
        self.assertIsNotNone(char)
        self.assertEqual(char["hp"]["current"], 12)


if __name__ == "__main__":
    unittest.main()
