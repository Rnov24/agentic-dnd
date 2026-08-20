"""
Unit tests for Dynamic Entity Context & Rules Agent Decoupling (Plan 018).
"""

import unittest
from agents.rules import RulesAgent
from agents.dm import DMAgent


class TestRulesDecoupling(unittest.TestCase):

    def setUp(self):
        self.rules = RulesAgent()
        self.dm = DMAgent()

    def test_dynamic_target_extraction_threats(self):
        context = {
            "threats": ["3 Redbrand Ruffians hiding behind barrels", "1 Goblin Boss"],
            "lighting": "dim light",
            "weather": "heavy rain"
        }
        actor = {"name": "Gundren", "equipment": ["Warhammer"]}
        
        # Test Redbrand target extraction
        res = self.rules.analyze_intent("I attack the redbrand ruffian", actor, context)
        self.assertEqual(res["action_type"], "combat_attack")
        self.assertEqual(res["target"], "redbrand")
        self.assertEqual(res["weapon"], "Warhammer")

    def test_dynamic_spellcasting_intent(self):
        context = {"threats": ["Nezznar the Black Spider"]}
        actor = {"name": "Eldrin", "cantrips": ["Fire Bolt", "Ray of Frost"]}
        
        res = self.rules.analyze_intent("I cast Ray of Frost at the spider", actor, context)
        self.assertEqual(res["action_type"], "spellcasting")
        self.assertEqual(res["spell_name"], "Ray of Frost")

    def test_dynamic_dm_narration(self):
        world_context = {
            "scene": {
                "name": "Cragmaw Castle",
                "lighting": "pitch darkness",
                "weather": "howling wind"
            }
        }
        check_result = {
            "action_type": "ability_check",
            "skill": "stealth",
            "dc": 12,
            "success": True,
            "formula": "1d20(15)+3"
        }
        narration = self.dm.narrate_turn(
            player_intent="I sneak along the north battlement",
            actor_name="Aria",
            world_context=world_context,
            check_result=check_result,
            attack_result=None,
            damage_result=None,
            npc_reaction=None,
            companion_reaction=None,
            state_changes_summary=[]
        )
        self.assertIn("Aria", narration)
        self.assertIn("Cragmaw Castle", narration)
        self.assertIn("pitch darkness", narration)


if __name__ == "__main__":
    unittest.main()
