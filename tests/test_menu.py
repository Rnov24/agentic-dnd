"""
Unit tests for Fast-Boot Context and Non-Developer Action Menu Engine.
"""

import unittest
import time
from tools.menu import get_boot_context, render_game_menu


class TestMenuEngine(unittest.TestCase):
    def test_fast_boot_context_latency_and_schema(self):
        # Cold start
        start = time.perf_counter()
        ctx = get_boot_context(force_refresh=True)
        elapsed_ms = (time.perf_counter() - start) * 1000

        # Performance check: cold load under 200ms
        self.assertLess(elapsed_ms, 200, f"Cold boot context took too long: {elapsed_ms:.2f}ms")

        # Warm start (cached) under 10ms
        start_warm = time.perf_counter()
        ctx_warm = get_boot_context()
        warm_ms = (time.perf_counter() - start_warm) * 1000
        self.assertLess(warm_ms, 10, f"Warm boot context took too long: {warm_ms:.2f}ms")

        # Schema checks
        self.assertIn("campaign_name", ctx)
        self.assertIn("location", ctx)
        self.assertIn("active_player", ctx)
        self.assertIn("party_roster", ctx)
        self.assertIn("scene", ctx)
        self.assertIn("in_combat", ctx)

    def test_render_game_menu_output(self):
        menu_str = render_game_menu()
        self.assertIn("GAME DASHBOARD", menu_str)
        self.assertIn("ACTIVE HERO", menu_str)
        self.assertIn("WHAT WOULD YOU LIKE TO DO?", menu_str)
        self.assertIn("TACTICAL & ROLEPLAY CHOICES", menu_str)
        self.assertIn("EXPLORATION & ENVIRONMENT", menu_str)
        self.assertIn("natural language", menu_str)

    def test_render_custom_context(self):
        fake_ctx = {
            "campaign_name": "Dragon of Icespire Peak",
            "location": "phandalin_town_square",
            "time_of_day": "Morning",
            "weather": "Sunny",
            "lighting": "Bright Light",
            "tension": "Peaceful",
            "in_combat": False,
            "scene": {
                "title": "Town Square",
                "description": "Villagers go about their morning routines.",
                "threats": ["Rumors of a white dragon"],
                "exits": ["Stonehill Inn", "Townmaster's Hall"]
            },
            "active_player": {
                "name": "Valeros",
                "level": 1,
                "class": "Fighter",
                "species": "Human",
                "ac": 16,
                "hp": {"current": 12, "max": 12, "temp": 0}
            },
            "party_roster": []
        }
        output = render_game_menu(fake_ctx)
        self.assertIn("DRAGON OF ICESPIRE PEAK", output)
        self.assertIn("phandalin_town_square", output)
        self.assertIn("Valeros", output)
        self.assertIn("Town Square", output)


if __name__ == "__main__":
    unittest.main()

