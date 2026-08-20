"""
Impact Agent for Agentic D&D.
Analyzes world-state mutations, detects consequential changes, and manages approval gates.
"""

from typing import Dict, Any
from tools.impact_analyzer import analyze_impact, ConsequentialReport, ImpactLevel


class ImpactAgent:
    """
    Evaluates turn state changes for irreversible or high-impact world events.
    """

    def evaluate_mutation(
        self,
        before_state: Dict[str, Any],
        proposed_state: Dict[str, Any],
        cause: str = "Player action"
    ) -> ConsequentialReport:
        """
        Determines if human approval is required before applying state mutation.
        """
        return analyze_impact(before_state, proposed_state, cause)
