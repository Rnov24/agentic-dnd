"""
Unit tests for Rules Explainer & Causal Orchestrator Traces (Plan 020).
"""

import unittest
from tools.explainer import explain_mechanic
from agents.orchestrator import ExecutionStep, ExecutionTrace


class TestExplainerAndCausalTraces(unittest.TestCase):

    def test_explain_weapon_mastery(self):
        res = explain_mechanic("topple")
        self.assertTrue(res["found"])
        self.assertEqual(res["topic"], "Topple")
        self.assertIn("saving throw", res["explanation"])

        res2 = explain_mechanic("vex")
        self.assertTrue(res2["found"])
        self.assertEqual(res2["topic"], "Vex")
        self.assertIn("Advantage", res2["explanation"])

    def test_explain_condition(self):
        res = explain_mechanic("prone")
        self.assertTrue(res["found"])
        self.assertIn("Prone", res["topic"])

    def test_explain_typo_suggestions(self):
        res = explain_mechanic("toppl")
        self.assertFalse(res["found"])
        self.assertIn("topple", res["suggestions"])

    def test_execution_trace_causal_graph(self):
        trace = ExecutionTrace(intent="I attack the goblin")
        s1 = ExecutionStep(step_id=1, agent="Orchestrator", action="Analyze intent")
        s2 = ExecutionStep(step_id=2, caused_by=1, agent="Rules Agent", action="Determine attack")
        s3 = ExecutionStep(step_id=3, caused_by=2, agent="Combat Tool", action="Roll attack")
        trace.steps.extend([s1, s2, s3])
        
        graph = trace.render_causal_graph()
        self.assertIn("Multi-Agent Lineage", graph)
        self.assertIn("#1 [Orchestrator] [root]", graph)
        self.assertIn("#2 [Rules Agent] [from #1]", graph)
        self.assertIn("#3 [Combat Tool] [from #2]", graph)


if __name__ == "__main__":
    unittest.main()
