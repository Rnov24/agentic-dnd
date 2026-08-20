"""
Unit tests for Mechanics Explainability, DC Breakdown & Damage Audit Cards (Plan 019).
"""

import unittest
from tools.mechanics import roll_check, roll_saving_throw
from tools.combat import roll_damage
from tools.formatting import render_mechanics_audit_card


class TestMechanicsExplainability(unittest.TestCase):

    def test_check_audit_breakdown(self):
        char = {
            "name": "Aria",
            "level": 3,
            "stats": {"dexterity": 16},
            "proficiencies": {"skills": ["stealth"]}
        }
        res = roll_check(char, skill="stealth", dc=15, seed=42)
        self.assertIn("audit_breakdown", res)
        self.assertIn("audit_explanation", res)
        self.assertIn("modifier_breakdown", res)
        self.assertEqual(res["modifier_breakdown"]["ability"], 3)
        self.assertEqual(res["modifier_breakdown"]["proficiency"], 2)
        self.assertTrue(len(res["audit_breakdown"]) >= 3)

    def test_saving_throw_audit_breakdown(self):
        char = {
            "name": "Valen",
            "level": 2,
            "stats": {"constitution": 14},
            "proficiencies": {"saving_throws": ["constitution"]}
        }
        res = roll_saving_throw(char, ability="constitution", dc=12, seed=42)
        self.assertIn("audit_breakdown", res)
        self.assertIn("audit_explanation", res)
        self.assertTrue(len(res["audit_breakdown"]) >= 3)

    def test_damage_audit_breakdown(self):
        attacker = {"name": "Aria", "stats": {"strength": 16}}
        target = {"name": "Skeleton", "vulnerabilities": ["bludgeoning"]}
        res = roll_damage(
            attacker=attacker,
            target=target,
            damage_formula="1d6",
            damage_type="bludgeoning",
            seed=42
        )
        self.assertIn("audit_breakdown", res)
        self.assertIn("audit_explanation", res)
        self.assertIn("vulnerable (2x)", res["multiplier_note"])

    def test_render_mechanics_audit_card(self):
        card = render_mechanics_audit_card(
            title="Stealth Check",
            breakdown_lines=["Base d20 Roll: 14", "DEX Modifier: +3", "Proficiency: +2"],
            outcome="19 vs DC 15 (SUCCESS)",
            is_success=True
        )
        self.assertIn("Stealth Check", card)
        self.assertIn("Outcome: ", card)


if __name__ == "__main__":
    unittest.main()
