"""
Theater of the Mind Zone-Based Spatial Combat Engine for Agentic D&D.
Provides tactical positioning, range validation, and movement adjudication
without requiring a strict 2D battle grid.
"""

from enum import Enum
from typing import Dict, Any, List, Optional, Tuple


class TacticalZone(str, Enum):
    ENGAGED = "engaged"   # Melee range (within 5 ft, in direct contact)
    CLOSE = "close"       # Short range (within 15 ft)
    NEAR = "near"         # Standard tactical range (15–30 ft)
    FAR = "far"           # Long range (30–60 ft+)


class SpatialCombatManager:
    """
    Manages combatant positions across Theater of the Mind spatial zones.
    """

    def __init__(self):
        self.positions: Dict[str, TacticalZone] = {}

    def assign_zone(self, combatant_id: str, zone: TacticalZone) -> None:
        """Assigns a combatant to a tactical zone."""
        clean_id = combatant_id.lower().replace(" ", "_")
        self.positions[clean_id] = zone

    def get_zone(self, combatant_id: str) -> TacticalZone:
        """Gets the current zone of a combatant, defaulting to ENGAGED."""
        clean_id = combatant_id.lower().replace(" ", "_")
        return self.positions.get(clean_id, TacticalZone.ENGAGED)

    def get_combatants_in_zone(self, zone: TacticalZone) -> List[str]:
        """Returns all combatant IDs currently occupying a given zone."""
        return [cid for cid, z in self.positions.items() if z == zone]

    def can_attack_target(
        self,
        attacker_id: str,
        target_id: str,
        weapon_type: str = "melee",
        reach_or_range: int = 5
    ) -> Tuple[bool, str]:
        """
        Adjudicates whether an attacker can reach a target based on relative zones.
        """
        attacker_zone = self.get_zone(attacker_id)
        target_zone = self.get_zone(target_id)

        # Same zone is always attackable
        if attacker_zone == target_zone:
            return True, f"Both combatants are in {attacker_zone.value} range."

        # Melee weapons with standard 5ft reach only reach ENGAGED with same zone
        if weapon_type.lower() == "melee":
            if reach_or_range <= 5:
                if attacker_zone != target_zone:
                    return False, f"Target is in '{target_zone.value}', out of 5ft melee reach from '{attacker_zone.value}'."
            elif reach_or_range <= 10:  # Reach weapons (Glaive, Halberd, Whip)
                if {attacker_zone, target_zone} == {TacticalZone.ENGAGED, TacticalZone.CLOSE}:
                    return True, "Reach weapon can strike between Engaged and Close zones."
                return False, f"Target is too far for reach weapon ({reach_or_range}ft)."

        # Ranged weapons & Spells
        # Range >= 60 can hit across all standard zones (Engaged to Far)
        if weapon_type.lower() in ["ranged", "spell", "thrown"]:
            if reach_or_range >= 60:
                return True, f"Target is within {reach_or_range}ft range ({target_zone.value})."
            elif reach_or_range >= 30:
                if target_zone == TacticalZone.FAR and attacker_zone == TacticalZone.ENGAGED:
                    return False, f"Target in '{target_zone.value}' is beyond {reach_or_range}ft range."
                return True, f"Target is within {reach_or_range}ft range."
            elif reach_or_range >= 15:
                if {attacker_zone, target_zone} <= {TacticalZone.ENGAGED, TacticalZone.CLOSE}:
                    return True, "Target is within short range."
                return False, f"Target is beyond {reach_or_range}ft short range."

        return True, "Attack is within range."

    def move_combatant(
        self,
        combatant_id: str,
        target_zone: TacticalZone,
        speed_ft: int = 30,
        has_dash: bool = False
    ) -> Dict[str, Any]:
        """
        Moves a combatant to a target zone, tracking distance and opportunity attack risk.
        """
        clean_id = combatant_id.lower().replace(" ", "_")
        current_zone = self.get_zone(clean_id)

        if current_zone == target_zone:
            return {
                "success": True,
                "combatant_id": clean_id,
                "previous_zone": current_zone.value,
                "new_zone": target_zone.value,
                "feet_moved": 0,
                "provokes_opportunity_attack": False,
                "message": f"Combatant is already in {target_zone.value}."
            }

        # Opportunity attack check: leaving ENGAGED zone
        provokes_oa = current_zone == TacticalZone.ENGAGED and target_zone != TacticalZone.ENGAGED

        # Zone step distance (1 step = ~15-30ft)
        zone_order = [TacticalZone.ENGAGED, TacticalZone.CLOSE, TacticalZone.NEAR, TacticalZone.FAR]
        curr_idx = zone_order.index(current_zone)
        target_idx = zone_order.index(target_zone)
        steps = abs(target_idx - curr_idx)
        distance_ft = steps * 15

        max_speed = speed_ft * (2 if has_dash else 1)
        if distance_ft > max_speed:
            return {
                "success": False,
                "combatant_id": clean_id,
                "error": f"Movement distance ({distance_ft}ft) exceeds max speed ({max_speed}ft).",
                "current_zone": current_zone.value
            }

        self.positions[clean_id] = target_zone
        return {
            "success": True,
            "combatant_id": clean_id,
            "previous_zone": current_zone.value,
            "new_zone": target_zone.value,
            "feet_moved": distance_ft,
            "provokes_opportunity_attack": provokes_oa,
            "message": f"Moved from {current_zone.value} to {target_zone.value} ({distance_ft}ft)."
        }
