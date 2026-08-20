"""
Unit tests for end-to-end multi-agent orchestration flow.
"""

import unittest
import shutil
import tempfile
from agents.orchestrator import OrchestratorAgent
from tools.state_manager import StateManager


class TestMultiAgentFlow(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.sm = StateManager(self.temp_dir)
        
        # Populate test party & NPCs
        self.sm.save_party([{
            "id": "aria",
            "name": "Aria Nightwind",
            "is_player": True,
            "stats": {"dexterity": 18},
            "proficiencies": {"skills": ["stealth", "sleight_of_hand"]}
        }])
        self.sm.save_npcs([{
            "id": "guard_karl",
            "name": "Guard Karl",
            "status": "Alive",
            "hp": {"current": 16, "max": 16}
        }])
        self.orchestrator = OrchestratorAgent(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_stealth_intent_orchestration(self):
        intent = "I sneak quietly past Guard Karl towards the cell door"
        trace = self.orchestrator.process_player_intent(intent, seed=42)
        
        self.assertTrue(trace.success)
        self.assertIsNotNone(trace.narration)
        self.assertGreater(len(trace.steps), 4)

        # Check that specific agents were invoked
        agent_names = [s.agent for s in trace.steps]
        self.assertIn("Orchestrator", agent_names)
        self.assertIn("World Agent", agent_names)
        self.assertIn("Rules Agent", agent_names)
        self.assertIn("Python Tool Runtime", agent_names)
        self.assertIn("NPC Agent", agent_names)
        self.assertIn("DM Agent", agent_names)
        self.assertIn("Git Versioning", agent_names)

    def test_attack_intent_orchestration(self):
        intent = "I stab Guard Karl with my dagger"
        trace = self.orchestrator.process_player_intent(intent, seed=42)
        self.assertTrue(trace.success)
        self.assertIn("Guard Karl", trace.narration)

    def test_spellcasting_intent_orchestration(self):
        # Add a wizard character
        self.sm.save_party([{
            "id": "rodolfo",
            "name": "Rodolfo Edinburgh",
            "class": "Wizard",
            "level": 1,
            "spell_slots": {"1": {"total": 2, "expended": 0}},
            "cantrips": ["Fire Bolt"],
            "spells_prepared": ["Magic Missile"],
            "stats": {"intelligence": 18}
        }])
        intent = "I cast Magic Missile at Guard Karl"
        trace = self.orchestrator.process_player_intent(intent, character_id="rodolfo", seed=42)
        self.assertTrue(trace.success)
        self.assertIsNotNone(trace.narration)
        step_actions = [s.action for s in trace.steps]
        self.assertTrue(any("Cast spell" in a for a in step_actions))

    def test_resting_intent_orchestration(self):
        self.sm.save_party([{
            "id": "aria",
            "name": "Aria Nightwind",
            "hp": {"current": 4, "max": 10, "temp": 0},
            "hit_dice": {"total": 1, "current": 1, "die": "1d8"},
            "stats": {"constitution": 12}
        }])
        intent = "We take a short rest and bandage our wounds"
        trace = self.orchestrator.process_player_intent(intent, seed=42)
        self.assertTrue(trace.success)
        step_actions = [s.action for s in trace.steps]
        self.assertTrue(any("Rest" in a for a in step_actions))


if __name__ == "__main__":
    unittest.main()
