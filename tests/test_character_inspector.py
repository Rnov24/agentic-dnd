"""
Unit tests for Character Inspection and Sheet Formatter.
"""

import unittest
from tools.character_inspector import CharacterInspector, compute_mod, format_mod


class TestCharacterInspector(unittest.TestCase):
    def setUp(self):
        self.inspector = CharacterInspector()

    def test_compute_and_format_mod(self):
        self.assertEqual(compute_mod(16), 3)
        self.assertEqual(format_mod(3), "+3")
        self.assertEqual(format_mod(-1), "-1")

    def test_inspect_existing_character(self):
        res = self.inspector.inspect_character("aria_nightwind")
        self.assertTrue(res["success"])
        self.assertEqual(res["character"]["name"], "Aria Nightwind")

    def test_render_character_sheet(self):
        res = self.inspector.inspect_character("aria_nightwind")
        sheet_text = self.inspector.render_character_sheet(res["character"])
        self.assertIn("ARIA NIGHTWIND", sheet_text.upper())
        self.assertIn("VITALS & DEFENSE", sheet_text)
        self.assertIn("ABILITY SCORES", sheet_text)


if __name__ == "__main__":
    unittest.main()
