"""
World Agent for Agentic D&D.
Maintains environmental state, lighting, weather, spatial layout, and global consequences.
"""

from typing import Dict, Any, List, Optional


class WorldAgent:
    """
    Simulates environmental factors, location dynamics, and physical world reactions.
    """

    def inspect_environment(self, world_state: Dict[str, Any], location_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Inspects the active location and returns environmental parameters and tactical features.
        """
        loc = location_id or world_state.get("active_location", "the_dungeon_cells")
        lighting = world_state.get("lighting", "dim flickering torchlight")
        weather = world_state.get("weather", "heavy rain and thunder")
        tension = world_state.get("tension_level", "high")
        alarm = world_state.get("alarm_raised", False)
        
        tactical_notes = []
        if "dim" in lighting.lower():
            tactical_notes.append("Shadows are long, granting favorable concealment for stealth.")
        if "rain" in weather.lower() or "thunder" in weather.lower():
            tactical_notes.append("Thunderclaps mask minor footstep sounds and metal clicks.")
        if alarm:
            tactical_notes.append("Fortress gong is echoing; sentries are actively patrolling.")
            
        return {
            "location_id": loc,
            "lighting": lighting,
            "weather": weather,
            "tension_level": tension,
            "alarm_raised": alarm,
            "tactical_notes": tactical_notes,
            "scene": world_state.get("current_scene", {}),
        }

    def update_environment_after_action(
        self,
        world_state: Dict[str, Any],
        action_summary: str,
        success: bool
    ) -> Dict[str, Any]:
        """
        Calculates environmental shifts based on player action results.
        """
        new_world = dict(world_state)
        flags = new_world.setdefault("global_flags", {})
        
        if "alarm" in action_summary.lower() or ("failed" in action_summary.lower() and "guard" in action_summary.lower()):
            new_world["tension_level"] = "extreme"
            
        return new_world
