"""
Unit tests for Encounter Difficulty & Adventuring Day XP Calculations.
Validates exact formulas and examples from D&D Basic Rules / DMG.
"""

import unittest
from tools.encounters import (
    calculate_encounter_difficulty,
    get_monster_count_multiplier,
    get_xp_by_cr,
    get_adventuring_day_budget,
    XP_THRESHOLDS_BY_LEVEL,
    ADVENTURING_DAY_XP,
    CR_TO_XP
)


class TestEncounterCalculations(unittest.TestCase):
    def test_xp_thresholds_table(self):
        """Validates all 20 character level threshold bounds."""
        self.assertEqual(len(XP_THRESHOLDS_BY_LEVEL), 20)
        self.assertEqual(XP_THRESHOLDS_BY_LEVEL[1]["easy"], 25)
        self.assertEqual(XP_THRESHOLDS_BY_LEVEL[1]["deadly"], 100)
        self.assertEqual(XP_THRESHOLDS_BY_LEVEL[3]["medium"], 150)
        self.assertEqual(XP_THRESHOLDS_BY_LEVEL[20]["deadly"], 12700)

    def test_multiplier_calculation_standard_party(self):
        """Tests standard 4-character party monster multipliers."""
        self.assertEqual(get_monster_count_multiplier(1, party_size=4), 1.0)
        self.assertEqual(get_monster_count_multiplier(2, party_size=4), 1.5)
        self.assertEqual(get_monster_count_multiplier(4, party_size=4), 2.0)
        self.assertEqual(get_monster_count_multiplier(8, party_size=4), 2.5)
        self.assertEqual(get_monster_count_multiplier(12, party_size=4), 3.0)
        self.assertEqual(get_monster_count_multiplier(16, party_size=4), 4.0)

    def test_multiplier_party_size_adjustments(self):
        """Tests small (<3) and large (6+) party size adjustments."""
        # Small party (<3) moves one step up
        self.assertEqual(get_monster_count_multiplier(1, party_size=2), 1.5)
        self.assertEqual(get_monster_count_multiplier(4, party_size=2), 2.5)
        
        # Large party (6+) moves one step down
        self.assertEqual(get_monster_count_multiplier(1, party_size=6), 0.5)
        self.assertEqual(get_monster_count_multiplier(4, party_size=6), 1.5)

    def test_official_dm_basic_rule_example(self):
        """
        Tests the official example from DMBasicRule.md line 5840-5870:
        Party: 3x Level 3 + 1x Level 2 (Party thresholds: Easy 275, Medium 550, Hard 825, Deadly 1400)
        Monsters: 1 Bugbear (200 XP) + 3 Hobgoblins (100 XP each)
        Base XP: 500 XP, 4 monsters -> Multiplier 2.0 -> Adjusted XP: 1000 XP
        Difficulty: Hard
        """
        party = [3, 3, 3, 2]
        monsters = [200, 100, 100, 100]
        
        result = calculate_encounter_difficulty(party, monsters)
        
        self.assertEqual(result["party_thresholds"]["easy"], 275)
        self.assertEqual(result["party_thresholds"]["medium"], 550)
        self.assertEqual(result["party_thresholds"]["hard"], 825)
        self.assertEqual(result["party_thresholds"]["deadly"], 1400)
        self.assertEqual(result["base_xp"], 500)
        self.assertEqual(result["multiplier"], 2.0)
        self.assertEqual(result["adjusted_xp"], 1000)
        self.assertEqual(result["difficulty"], "Hard")

    def test_situational_modifiers(self):
        """Tests situational modifiers shifting difficulty step up or down."""
        party = [3, 3, 3, 2]
        monsters = [200, 100, 100, 100] # normally Hard (1000 XP)
        
        # Drawback (+1) shifts Hard -> Deadly
        res_drawback = calculate_encounter_difficulty(party, monsters, situational_modifier=1)
        self.assertEqual(res_drawback["difficulty"], "Deadly")
        
        # Benefit (-1) shifts Hard -> Medium
        res_benefit = calculate_encounter_difficulty(party, monsters, situational_modifier=-1)
        self.assertEqual(res_benefit["difficulty"], "Medium")

    def test_adventuring_day_budget(self):
        """Tests adventuring day budget summing."""
        party = [3, 3, 3, 2] # 3x 1200 + 1x 600 = 4200 XP
        budget = get_adventuring_day_budget(party)
        self.assertEqual(budget, 4200)

    def test_cr_to_xp_lookup(self):
        """Tests CR to base XP mapping."""
        self.assertEqual(get_xp_by_cr("1/4"), 50)
        self.assertEqual(get_xp_by_cr("1"), 200)
        self.assertEqual(get_xp_by_cr("17"), 18000)

    def test_preset_encounters(self):
        """Tests evaluating adventure preset encounters."""
        from tools.encounters import evaluate_preset_encounter, get_preset_encounter
        preset = get_preset_encounter("goblin_ambush")
        self.assertIsNotNone(preset)
        self.assertEqual(preset.get("name"), "Goblin Ambush on Triboar Trail")

        res = evaluate_preset_encounter("goblin_ambush", party_levels=[1, 1, 1, 1])
        self.assertTrue(res["success"])
        self.assertEqual(res["monster_count"], 4)
        self.assertEqual(res["base_xp"], 200)
        self.assertIn("goblins", res["tactics"].lower())


if __name__ == "__main__":
    unittest.main()
