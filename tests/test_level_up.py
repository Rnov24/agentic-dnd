"""
Unit tests for Level-Up Progression Engine.
"""

import unittest
from tools.character_creator import CharacterCreator
from tools.level_up import LevelUpManager, get_proficiency_bonus


class TestLevelUp(unittest.TestCase):
    def setUp(self):
        self.creator = CharacterCreator()
        self.lum = LevelUpManager()

    def test_proficiency_bonus_progression(self):
        self.assertEqual(get_proficiency_bonus(1), 2)
        self.assertEqual(get_proficiency_bonus(4), 2)
        self.assertEqual(get_proficiency_bonus(5), 3)
        self.assertEqual(get_proficiency_bonus(8), 3)
        self.assertEqual(get_proficiency_bonus(9), 4)
        self.assertEqual(get_proficiency_bonus(13), 5)
        self.assertEqual(get_proficiency_bonus(17), 6)

    def test_level_up_fighter_average_hp(self):
        char = self.creator.create_character(
            name="Garen",
            char_class="Fighter",
            species="Human",
            background="Soldier",
            custom_scores={"strength": 15, "dexterity": 13, "constitution": 14, "intelligence": 10, "wisdom": 12, "charisma": 8}
        )
        # CON becomes 15 (+2 mod). Lvl 1 HP = 10 + 2 = 12.
        self.assertEqual(char["hp"]["max"], 12)
        
        # Level up to 2
        res = self.lum.level_up_character("garen", hp_choice="average")
        self.assertTrue(res["success"])
        self.assertEqual(res["new_level"], 2)
        # Fighter hit die is 1d10. Avg = 6. CON mod = 2. HP gain = 8.
        self.assertEqual(res["hp_gain"], 8)
        self.assertTrue(any("Action Surge" in f for f in res["character"]["features"]))

    def test_level_up_wizard_spell_slots(self):
        char = self.creator.create_character(
            name="Morgath",
            char_class="Wizard",
            species="High Elf",
            background="Sage",
            custom_scores={"strength": 8, "dexterity": 14, "constitution": 12, "intelligence": 15, "wisdom": 13, "charisma": 10}
        )
        self.assertEqual(char["level"], 1)
        self.assertEqual(char["spell_slots"]["level_1"]["max"], 2)

        # Level up to 2
        self.lum.level_up_character("morgath")
        char_lvl2 = self.lum.sm.get_character("morgath")
        self.assertEqual(char_lvl2["spell_slots"]["level_1"]["max"], 3)

        # Level up to 3
        self.lum.level_up_character("morgath")
        char_lvl3 = self.lum.sm.get_character("morgath")
        self.assertEqual(char_lvl3["spell_slots"]["level_1"]["max"], 4)
        self.assertEqual(char_lvl3["spell_slots"]["level_2"]["max"], 2)


if __name__ == "__main__":
    unittest.main()
