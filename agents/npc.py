"""
NPC Agent for Agentic D&D.
Maintains persistent NPC memory, personality, disposition, dialogue, and behavioral reactions.
"""

from typing import Dict, Any, List, Optional


class NPCAgent:
    """
    Evaluates NPC awareness, dialogue responses, and behavior based on persistent state.
    """

    def evaluate_reaction(
        self,
        npc: Dict[str, Any],
        player_action: str,
        check_result: Optional[Dict[str, Any]],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Determines how an NPC reacts to a player action and check outcome.
        """
        npc_id = npc.get("id", "npc")
        npc_name = npc.get("name", "NPC")
        disposition = npc.get("disposition", "Neutral")
        
        reaction_text = ""
        new_disposition = disposition
        alert_triggered = False
        dialogue = ""
        
        # 1. Guard Karl in the Dungeon
        if npc_id == "guard_karl":
            if check_result and check_result.get("action_type") in ["ability_check", "check"]:
                is_success = check_result.get("success", False)
                if is_success:
                    reaction_text = "Guard Karl snores softly against the barrel, completely oblivious to the stealthy intrusion."
                    dialogue = "*snore* ...five more minutes on watch..."
                else:
                    reaction_text = "Guard Karl jolts awake at the scuffing sound, knocking his lantern askew and gripping his spear!"
                    new_disposition = "Hostile / Alert"
                    alert_triggered = True
                    dialogue = "Who's there?! Halts, in the name of Captain Aldric!"
            elif "attack" in player_action.lower():
                reaction_text = "Guard Karl screams in pain and brandishes his spear in self defense!"
                new_disposition = "Hostile"
                dialogue = "Intruders in the cellblock! Sound the alarm!"
                
        # 2. Prisoner Valen
        elif npc_id == "prisoner_valen":
            if "free" in player_action.lower() or "unlock" in player_action.lower() or "pick" in player_action.lower():
                reaction_text = "Valen clutches the cell bars in breathless anticipation, tears gleaming in his soot-stained eyes."
                dialogue = "By the stars... you actually made it. The drainage grate behind me leads to the ravine—be quick!"
            else:
                dialogue = "Please... the Captain will return at midnight. We don't have much time."
                
        # 3. Captain Aldric
        elif npc_id == "captain_aldric":
            if "attack" in player_action.lower():
                reaction_text = "Captain Aldric unslings his massive two-handed greatsword with cold, lethal precision."
                dialogue = "Rebel scum. You will hang from the highest rampart by morning."
            else:
                dialogue = "Stand down and throw your weapons to the stone, or bleed where you stand."

        # Default fallback
        if not reaction_text:
            reaction_text = f"{npc_name} observes the situation carefully."
            
        return {
            "npc_id": npc_id,
            "npc_name": npc_name,
            "previous_disposition": disposition,
            "new_disposition": new_disposition,
            "alert_triggered": alert_triggered,
            "reaction_summary": reaction_text,
            "dialogue": dialogue,
        }
