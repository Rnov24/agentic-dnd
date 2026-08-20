"""
Dungeon Master (DM) Agent for Agentic D&D.
Generates atmospheric, evocative Theater-of-the-Mind narration honoring deterministic rules outcomes.
"""

from typing import Dict, Any, List, Optional


class DMAgent:
    """
    The primary narrative intelligence of the game.
    Weaves environmental factors, mechanical results, NPC dialogues, and pacing.
    """

    def narrate_turn(
        self,
        player_intent: str,
        actor_name: str,
        world_context: Dict[str, Any],
        check_result: Optional[Dict[str, Any]],
        attack_result: Optional[Dict[str, Any]],
        damage_result: Optional[Dict[str, Any]],
        npc_reaction: Optional[Dict[str, Any]],
        companion_reaction: Optional[Dict[str, Any]],
        state_changes_summary: List[str],
        spell_result: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Synthesizes all multi-agent outputs into a rich Theater-of-the-Mind narration.
        """
        narration_parts = []
        
        # 1. Action & Mechanical Resolution
        scene = world_context.get("scene", {})
        lighting = scene.get("lighting", world_context.get("lighting", "ambient light"))
        weather = scene.get("weather", world_context.get("weather", "clear"))
        location = scene.get("name", world_context.get("active_location", "the area"))

        if check_result and check_result.get("action_type") in ["ability_check", "check"]:
            skill = check_result.get("skill") or check_result.get("ability", "check")
            dc = check_result.get("dc", 15)
            is_success = check_result.get("success", False)
            formula = check_result.get("formula", "")
            
            if is_success:
                if skill == "stealth":
                    narration_parts.append(
                        f"Moving through the {lighting} amidst the {weather}, {actor_name} glides silently through {location}. "
                        f"Footsteps leave barely a whisper in the air `[Stealth Check: {formula} vs DC {dc} - SUCCESS]`."
                    )
                elif skill == "sleight_of_hand":
                    narration_parts.append(
                        f"With surgical precision, {actor_name}'s fingers execute the fine motion with complete poise, "
                        f"leaving no trace of manipulation `[Sleight of Hand: {formula} vs DC {dc} - SUCCESS]`."
                    )
                elif skill == "investigation":
                    narration_parts.append(
                        f"{actor_name}'s keen eyes scour {location}, quickly identifying structural details and hidden clues "
                        f"`[Investigation: {formula} vs DC {dc} - SUCCESS]`."
                    )
                else:
                    narration_parts.append(
                        f"{actor_name} successfully executes the maneuver with poise and precision `[{skill.capitalize()} Check: {formula} vs DC {dc} - SUCCESS]`."
                    )
            else:
                narration_parts.append(
                    f"A sudden misstep echoes in {location} as composure momentarily slips `[{skill.capitalize()} Check: {formula} vs DC {dc} - FAILURE]`!"
                )
                
        elif attack_result:
            is_hit = attack_result.get("is_hit", False)
            formula = attack_result.get("formula", "")
            target = attack_result.get("target", "target").replace("_", " ").title()
            weapon = attack_result.get("attack_name", "weapon")
            
            if is_hit:
                dmg_total = damage_result.get("final_damage", 0) if damage_result else 0
                crit_text = " **CRITICAL HIT!**" if attack_result.get("is_critical_hit") else ""
                narration_parts.append(
                    f"{actor_name} strikes forward with {weapon}{crit_text}! The blow connects cleanly against {target} "
                    f"`[Attack: {formula} vs AC {attack_result.get('target_ac')} - HIT! Deal {dmg_total} damage]`."
                )
            else:
                narration_parts.append(
                    f"{actor_name} lunges with {weapon}, but the attack is deflected by {target}'s guard "
                    f"`[Attack: {formula} vs AC {attack_result.get('target_ac')} - MISS]`."
                )
        elif spell_result:
            s_name = spell_result.get("spell_name") or spell_result.get("spell", "spell")
            dmg = spell_result.get("damage")
            heal = spell_result.get("healing")
            tgt = spell_result.get("target_name") or "the target"
            if dmg:
                dmg_type = spell_result.get("damage_type", "magical")
                narration_parts.append(
                    f"{actor_name} unleashes {s_name} with crackling magical power! The energy strikes {tgt} `[Cast {s_name}: {dmg} {dmg_type} damage]`."
                )
            elif heal:
                narration_parts.append(
                    f"{actor_name} channels restorative magic, casting {s_name}! Soothing light washes over {tgt} `[Cast {s_name}: +{heal} HP]`."
                )
            else:
                narration_parts.append(
                    f"{actor_name} weaves arcane energies to cast {s_name} targeting {tgt} `[Cast {s_name}]`."
                )
        else:
            narration_parts.append(f"{actor_name} {player_intent.rstrip('.')} with calculated care.")

        # 2. NPC Dialogue & Reactions
        if npc_reaction:
            react_summary = npc_reaction.get("reaction_summary")
            dialogue = npc_reaction.get("dialogue")
            if react_summary:
                narration_parts.append(f"\n{react_summary}")
            if dialogue:
                narration_parts.append(f'\n> **{npc_reaction.get("npc_name", "NPC")}**: "{dialogue}"')

        # 3. Companion Commentary
        if companion_reaction:
            comp_dialogue = companion_reaction.get("dialogue")
            comp_name = companion_reaction.get("name", "Companion")
            if comp_dialogue:
                narration_parts.append(f'\n> **{comp_name}**: "{comp_dialogue}"')

        # 4. Sensory / Theater-of-the-Mind Scene Context & Next Action Prompts
        scene = world_context.get("scene", {})
        threats = scene.get("threats", [])
        exits = scene.get("exits", [])
        
        narration_parts.append("\n---")
        narration_parts.append("**What do you do next?**")
        
        return "\n".join(narration_parts)
