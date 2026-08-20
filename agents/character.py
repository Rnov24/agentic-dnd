"""
Character Agent for Agentic D&D.
Controls autonomous AI companions (party members), providing authentic personality,
tactical assists, and roleplay banter.
"""

from typing import Dict, Any, List, Optional


class CharacterAgent:
    """
    Simulates AI companion party members with distinct personas and agency.
    """

    def generate_companion_reaction(
        self,
        companion: Dict[str, Any],
        player_intent: str,
        turn_result: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Determines companion commentary, magical assists, or tactical support.
        """
        comp_id = companion.get("id", "companion")
        name = companion.get("name", "Companion")
        
        # Eldrin the Wizard
        if comp_id == "eldrin_shadowseeker":
            if "sneak" in player_intent.lower() or "stealth" in player_intent.lower():
                return {
                    "companion_id": comp_id,
                    "name": name,
                    "action": "casts Minor Illusion / whispers arcane words to muffle footfalls",
                    "dialogue": "*whispers* I have an arcane lockpick spell prepared if the iron tumbler jams, Aria.",
                }
            elif "attack" in player_intent.lower() or "combat" in player_intent.lower():
                return {
                    "companion_id": comp_id,
                    "name": name,
                    "action": "channels arcane energy, preparing Fire Bolt from the shadows",
                    "dialogue": "Watch your flank! I'll cover your retreat with evocation!",
                }
            else:
                return {
                    "companion_id": comp_id,
                    "name": name,
                    "action": "studies the ancient mortar and runes along the corridor wall",
                    "dialogue": "These stones date back to the early dynasty. Fascinating craftsmanship.",
                }
                
        return None
