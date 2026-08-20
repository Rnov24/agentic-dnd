"""
Unit tests for Character Creation Engine.
"""

import unittest
from tools.character_creator import CharacterCreator, compute_modifier, generate_scores


class TestCharacterCreator(unittest.TestCase):
    def setUp(self):
        self.creator = CharacterCreator()

    def test_compute_modifier(self):
        self.assertEqual(compute_modifier(10), 0)
        self.assertEqual(compute_modifier(14), 2)
        self.assertEqual(compute_modifier(8), -1)
        self.assertEqual(compute_modifier(18), 4)

    def test_generate_scores_standard(self):
        scores = generate_scores("standard")
        self.assertEqual(scores, [15, 14, 13, 12, 10, 8])

    def test_generate_scores_roll(self):
        scores = generate_scores("roll", seed=42)
        self.assertEqual(len(scores), 6)
        for s in scores:
            self.assertGreaterEqual(s, 3)
            self.assertLessEqual(s, 18)

    def test_create_fighter(self):
        char = self.creator.create_character(
            name="Thorin Ironbreaker",
            char_class="Fighter",
            species="Hill Dwarf",
            background="Soldier",
            method="standard"
        )
        self.assertEqual(char["name"], "Thorin Ironbreaker")
        self.assertEqual(char["class"], "Fighter")
        self.assertEqual(char["species"], "Hill Dwarf")
        self.assertEqual(char["level"], 1)
        # Hill Dwarf gives +2 CON, +1 WIS. Base CON=14->16.
        self.assertEqual(char["stats"]["constitution"], 16)
        # 10 base + 3 CON mod + 1 Dwarven Toughness = 14 HP
        self.assertEqual(char["hp"]["max"], 14)
        self.assertEqual(char["hit_dice"]["die"], "1d10")
        self.assertIn("athletics", char["skills"])

    def test_create_wizard_spellcaster(self):
        char = self.creator.create_character(
            name="Archimedes",
            char_class="Wizard",
            species="Elf",
            background="Sage",
            method="standard"
        )
        self.assertEqual(char["class"], "Wizard")
        self.assertIn("spellcasting", char)
        self.assertIn("cantrips", char)
        self.assertEqual(char["spell_slots"]["level_1"]["max"], 2)

    def test_validate_point_buy(self):
        from tools.character_creator import validate_point_buy
        valid_scores = {"strength": 15, "dexterity": 14, "constitution": 13, "intelligence": 12, "wisdom": 10, "charisma": 8}
        is_valid, cost, msg = validate_point_buy(valid_scores)
        self.assertTrue(is_valid)
        self.assertEqual(cost, 27)

    def test_create_lmop_preset(self):
        char = self.creator.create_character(name=None, preset="lmop_rogue_criminal")
        self.assertEqual(char["name"], "Aria Nightwind")
        self.assertEqual(char["class"], "Rogue")
        self.assertEqual(char["species"], "Lightfoot Halfling")
        self.assertIn("personality", char)
        self.assertIn("traits", char["personality"])

    def test_create_monk_unarmored_ac(self):
        char = self.creator.create_character(
            name="Li Wei",
            char_class="Monk",
            species="Human",
            background="Acolyte",
            custom_scores={"strength": 10, "dexterity": 15, "constitution": 12, "intelligence": 10, "wisdom": 14, "charisma": 8}
        )
        # Human adds +1: DEX=16 (+3 mod), WIS=15 (+2 mod). Monk AC = 10 + 3 + 2 = 15.
        self.assertEqual(char["ac"], 15)
        self.assertEqual(char["hit_dice"]["die"], "1d8")


if __name__ == "__main__":
    unittest.main()
