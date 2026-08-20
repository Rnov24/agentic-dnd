"""
Unit tests for Fuzzy Suggestions & Error Recovery Engine.
"""

import unittest
from tools.suggestions import suggest_closest, suggest_skill, suggest_spell


class TestSuggestions(unittest.TestCase):

    def test_suggest_skill_typos(self):
        # stealth typo
        suggs = suggest_skill("stealt")
        self.assertIn("Stealth", suggs)

        # perception typo
        suggs = suggest_skill("percepton")
        self.assertIn("Perception", suggs)

        # acrobatics typo
        suggs = suggest_skill("acrobatic")
        self.assertIn("Acrobatics", suggs)

    def test_suggest_spell_typos(self):
        # Fire bolt typo
        suggs = suggest_spell("fireblt")
        self.assertIn("Fire Bolt", suggs)

        # Magic missile typo
        suggs = suggest_spell("missile")
        self.assertIn("Magic Missile", suggs)

    def test_suggest_fallback(self):
        suggs = suggest_skill("completely_unknown_xyz")
        self.assertGreater(len(suggs), 0)


if __name__ == "__main__":
    unittest.main()
