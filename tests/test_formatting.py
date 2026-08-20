"""
Unit tests for visual formatting and health bar rendering.
"""

import unittest
from tools.formatting import render_hp_bar, render_slot_pips, badge, box_header, format_dialogue


class TestFormatting(unittest.TestCase):
    def test_render_hp_bar(self):
        bar_full = render_hp_bar(10, 10)
        self.assertIn("10/10 HP", bar_full)
        bar_half = render_hp_bar(5, 10, temp=2)
        self.assertIn("5/10 HP", bar_half)
        self.assertIn("(+2 Temp)", bar_half)

    def test_render_slot_pips(self):
        pips = render_slot_pips(2, 4)
        self.assertIn("2/4", pips)

    def test_badges(self):
        b_succ = badge("SUCCESS", "success")
        self.assertIn("SUCCESS", b_succ)
        b_crit = badge("CRITICAL", "crit")
        self.assertIn("CRITICAL", b_crit)

    def test_format_dialogue(self):
        diag = format_dialogue("Sildar", "Follow me!", role="Knight")
        self.assertIn("Sildar", diag)
        self.assertIn("Follow me!", diag)

    def test_render_state_diff(self):
        from tools.formatting import render_state_diff
        sample_diff = {
            "party": {"hp": {"before": 10, "after": 6}},
            "world": {"tension_level": {"before": "Calm", "after": "High"}}
        }
        diff_str = render_state_diff(sample_diff)
        self.assertIn("CAMPAIGN STATE DIFF", diff_str)
        self.assertIn("PARTY", diff_str)
        self.assertIn("WORLD", diff_str)

    def test_render_turn_mini_hud(self):
        from tools.formatting import render_turn_mini_hud
        actor = {"name": "Rodolfo", "level": 1, "class": "Wizard", "hp": {"current": 7, "max": 7}}
        hud = render_turn_mini_hud(actor)
        self.assertIn("TURN HUD", hud)
        self.assertIn("Rodolfo", hud)
        self.assertIn("7/7", hud)


if __name__ == "__main__":
    unittest.main()
