"""
Consequential Change Impact Analyzer for Agentic D&D.
Classifies proposed game-state mutations into LOW (auto-approved) vs HIGH (requires human approval).
Generates structured approval payloads with diffs and affected entity breakdowns.
"""

from enum import Enum
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


class ImpactLevel(str, Enum):
    LOW = "LOW"
    HIGH = "HIGH"


@dataclass
class ConsequentialReport:
    is_consequential: bool
    impact_level: ImpactLevel
    title: str
    action: str
    cause: str
    affected_files: List[str]
    before_summary: str
    after_summary: str
    diff_details: Dict[str, Any] = field(default_factory=dict)
    requires_approval: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_consequential": self.is_consequential,
            "impact_level": self.impact_level.value,
            "title": self.title,
            "action": self.action,
            "cause": self.cause,
            "affected_files": self.affected_files,
            "before_summary": self.before_summary,
            "after_summary": self.after_summary,
            "diff_details": self.diff_details,
            "requires_approval": self.requires_approval,
        }


MAJOR_NPCS = {"captain_aldric", "goblin_king_gresh", "prisoner_valen", "mira_the_alchemist"}
IMPORTANT_ITEMS = {"black_glass_dagger", "fortress_iron_key", "aldrics_greatsword"}


def analyze_impact(
    before_state: Dict[str, Any],
    proposed_state: Dict[str, Any],
    cause: str = "Player action",
) -> ConsequentialReport:
    """
    Compares the state before and after a proposed turn/action and determines
    if high-impact human approval is mandated by the D&D ruleset & safety policies.
    """
    affected_files: List[str] = []
    high_impact_reasons: List[str] = []
    
    # 1. Check Character Deaths or 0 HP
    before_party = {c.get("id"): c for c in before_state.get("party", [])}
    after_party = {c.get("id"): c for c in proposed_state.get("party", [])}
    
    for c_id, after_char in after_party.items():
        before_char = before_party.get(c_id, {})
        before_hp = before_char.get("hp", {}).get("current", 10)
        after_hp = after_char.get("hp", {}).get("current", 10)
        char_name = after_char.get("name", c_id)
        
        # Check Death Condition
        after_conds = [c.lower() for c in after_char.get("conditions", [])]
        before_conds = [c.lower() for c in before_char.get("conditions", [])]
        
        if "dead" in after_conds and "dead" not in before_conds:
            high_impact_reasons.append(f"Permanent death of Player Character: {char_name}")
            affected_files.append(f"campaign/characters/{c_id}.md")
            affected_files.append("state/party.json")
        elif after_hp == 0 and before_hp > 0:
            high_impact_reasons.append(f"Player Character {char_name} fell unconscious to 0 HP")
            affected_files.append(f"campaign/characters/{c_id}.md")
            
    # 2. Check Major NPC Deaths
    def _extract_npcs(npcs_obj):
        if isinstance(npcs_obj, dict):
            return {str(k): v for k, v in npcs_obj.items() if isinstance(v, dict)}
        elif isinstance(npcs_obj, list):
            res = {}
            for n in npcs_obj:
                if isinstance(n, dict):
                    nid = str(n.get("id") or n.get("name", "unknown")).lower()
                    res[nid] = n
            return res
        return {}

    before_npcs = _extract_npcs(before_state.get("npcs", []))
    after_npcs = _extract_npcs(proposed_state.get("npcs", []))
    
    for n_id, after_npc in after_npcs.items():
        before_npc = before_npcs.get(n_id, {})
        npc_name = after_npc.get("name", n_id)
        
        before_status = before_npc.get("status", "Alive")
        after_status = after_npc.get("status", "Alive")
        after_hp = after_npc.get("hp", {}).get("current", 10) if isinstance(after_npc.get("hp"), dict) else 10
        
        is_major = (n_id and str(n_id).lower() in MAJOR_NPCS) or after_npc.get("is_boss", False) or after_npc.get("role") == "Major"
        
        if (after_status == "Dead" or after_hp <= 0) and before_status != "Dead":
            if is_major:
                high_impact_reasons.append(f"Death of Major NPC: {npc_name}")
                affected_files.append(f"campaign/npcs/{n_id}.md")
                affected_files.append("state/npcs.json")
                
    # 3. Check Quest Permanent Failure
    def _extract_quests(quests_obj):
        if isinstance(quests_obj, dict):
            q_list = quests_obj.get("active_quests", []) + quests_obj.get("completed_quests", [])
            return {q.get("id"): q for q in q_list if isinstance(q, dict)}
        elif isinstance(quests_obj, list):
            return {q.get("id"): q for q in quests_obj if isinstance(q, dict)}
        return {}

    before_quests = _extract_quests(before_state.get("quests", []))
    after_quests = _extract_quests(proposed_state.get("quests", []))
    
    for q_id, after_q in after_quests.items():
        before_q = before_quests.get(q_id, {})
        if after_q.get("status") == "Failed" and before_q.get("status") != "Failed":
            high_impact_reasons.append(f"Permanent Quest Failure: {after_q.get('title', q_id)}")
            affected_files.append(f"campaign/quests/{q_id}.md")
            affected_files.append("state/quests.json")
            
    # 4. Check Major World Flags / Destruction
    before_world = before_state.get("world", {})
    after_world = proposed_state.get("world", {})
    
    if after_world.get("alarm_raised") and not before_world.get("alarm_raised"):
        high_impact_reasons.append("Fortress Alarm Raised: Royal Garrison on High Alert")
        affected_files.append("campaign/factions/royal_garrison.md")
        affected_files.append("state/world.json")
        
    if high_impact_reasons:
        return ConsequentialReport(
            is_consequential=True,
            impact_level=ImpactLevel.HIGH,
            title="Consequential World State Mutation",
            action="; ".join(high_impact_reasons),
            cause=cause,
            affected_files=list(set(affected_files)),
            before_summary="Entities were alive/active in baseline state.",
            after_summary="Permanent state shift occurred: " + "; ".join(high_impact_reasons),
            diff_details={"reasons": high_impact_reasons},
            requires_approval=True,
        )
        
    return ConsequentialReport(
        is_consequential=False,
        impact_level=ImpactLevel.LOW,
        title="Routine State Transition",
        action="Standard gameplay progression",
        cause=cause,
        affected_files=affected_files,
        before_summary="Routine state",
        after_summary="Routine update applied automatically",
        diff_details={},
        requires_approval=False,
    )
