"""
Central Orchestrator Agent for Agentic D&D.
Deconstructs natural-language player intent, coordinates specialized sub-agents,
executes deterministic Python tools, manages state persistence, and audits execution traces.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field, asdict
import time

from agents.dm import DMAgent
from agents.rules import RulesAgent
from agents.combat import CombatAgent
from agents.npc import NPCAgent
from agents.world import WorldAgent
from agents.character import CharacterAgent
from agents.impact import ImpactAgent
from tools.state_manager import StateManager
from tools.git_versioning import CampaignGitManager
from tools.mechanics import roll_check
from tools.combat import roll_attack, roll_damage, apply_damage, apply_healing
from tools.spells import cast_spell
from tools.resting import execute_short_rest, execute_long_rest
from tools.permissions import PermissionManager, RuntimeMode


@dataclass
class ExecutionStep:
    agent: str
    action: str
    details: Dict[str, Any] = field(default_factory=dict)
    step_id: int = 0
    caused_by: Optional[int] = None
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "caused_by": self.caused_by,
            "agent": self.agent,
            "action": self.action,
            "details": self.details,
            "timestamp": self.timestamp,
        }


@dataclass
class ExecutionTrace:
    intent: str
    steps: List[ExecutionStep] = field(default_factory=list)
    narration: str = ""
    requires_approval: bool = False
    approval_payload: Optional[Dict[str, Any]] = None
    commit_id: Optional[str] = None
    success: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "intent": self.intent,
            "steps": [s.to_dict() for s in self.steps],
            "narration": self.narration,
            "requires_approval": self.requires_approval,
            "approval_payload": self.approval_payload,
            "commit_id": self.commit_id,
            "success": self.success,
        }

    def render_causal_graph(self) -> str:
        """Renders an ASCII causal execution graph showing multi-agent decision flow."""
        lines = [f"┌── Multi-Agent Lineage: > {self.intent}"]
        for s in self.steps:
            parent_str = f" [from #{s.caused_by}]" if s.caused_by is not None else " [root]"
            lines.append(f"│  #{s.step_id} [{s.agent}]{parent_str} ➔ {s.action}")
        lines.append("└" + "─" * 55)
        return "\n".join(lines)


class OrchestratorAgent:
    """
    Coordinates multi-agent game orchestration and tool dispatch.
    """

    def __init__(self, base_dir: Optional[str] = None, mode: RuntimeMode = RuntimeMode.GAME_MODE):
        self.state_manager = StateManager(base_dir)
        self.git_manager = CampaignGitManager(base_dir)
        self.permission_manager = PermissionManager(mode)
        
        self.dm_agent = DMAgent()
        self.rules_agent = RulesAgent()
        self.combat_agent = CombatAgent()
        self.npc_agent = NPCAgent()
        self.world_agent = WorldAgent()
        self.character_agent = CharacterAgent()
        self.impact_agent = ImpactAgent()

    def _add_step(
        self,
        trace: ExecutionTrace,
        agent: str,
        action: str,
        details: Dict[str, Any],
        caused_by: Optional[int] = None
    ) -> ExecutionStep:
        step_id = len(trace.steps) + 1
        step = ExecutionStep(
            step_id=step_id,
            caused_by=caused_by,
            agent=agent,
            action=action,
            details=details,
        )
        trace.steps.append(step)
        return step

    def process_player_intent(
        self,
        intent: str,
        character_id: Optional[str] = None,
        seed: Optional[int] = None,
        auto_commit: bool = True
    ) -> ExecutionTrace:
        """
        Executes a complete multi-agent turn loop for a player's natural language intent.
        """
        trace = ExecutionTrace(intent=intent)
        
        # 1. Inspect State & Active Actor
        party = self.state_manager.get_party()
        world_state = self.state_manager.get_world()
        actor = None
        if character_id:
            actor = self.state_manager.get_character(character_id)
        if not actor and world_state.get("active_character_id"):
            actor = self.state_manager.get_character(world_state["active_character_id"])
        if not actor and party:
            actor = party[0]  # Default to primary player character (e.g. Aria)
        if not actor:
            actor = {"id": "aria_nightwind", "name": "Aria Nightwind", "stats": {"dexterity": 17}}
        npcs = self.state_manager.get_npcs()
        before_snapshot = self.state_manager.get_full_state()
        
        s1 = self._add_step(
            trace=trace,
            agent="Orchestrator",
            action="Analyze player intent and inspect current campaign context",
            details={
                "actor": actor.get("name"),
                "intent": intent,
                "location": world_state.get("active_location"),
            },
            caused_by=None
        )
        
        # 2. World Agent -> Environmental Context
        env_context = self.world_agent.inspect_environment(world_state)
        s2 = self._add_step(
            trace=trace,
            agent="World Agent",
            action="Inspect active location environment and tactical modifiers",
            details=env_context,
            caused_by=s1.step_id
        )
        
        # 3. Rules Agent -> Evaluate Mechanics
        rules_analysis = self.rules_agent.analyze_intent(intent, actor, env_context)
        s3 = self._add_step(
            trace=trace,
            agent="Rules Agent",
            action="Determine D&D 5e (2024) checks, DCs, and action requirements",
            details=rules_analysis,
            caused_by=s2.step_id
        )
        
        check_result = None
        attack_result = None
        damage_result = None
        spell_result = None
        tool_calls_record = []
        last_tool_step = s3
        
        # 4. Python Tool Runtime -> Deterministic Execution
        if rules_analysis.get("action_type") == "spellcasting":
            target_name = rules_analysis.get("target", "enemy")
            target_npc = self.state_manager.get_npc(target_name) or {
                "name": target_name.replace("_", " ").title(), "ac": 13, "hp": {"current": 10, "max": 10}
            }
            spell_result = cast_spell(
                caster=actor,
                spell_name=rules_analysis.get("spell_name", "Fire Bolt"),
                target=target_npc,
                seed=seed
            )
            tool_calls_record.append({"tool": "spells.cast_spell", "output": spell_result})
            self.state_manager.update_character(actor)
            if target_npc and target_npc.get("id"):
                self.state_manager.update_npc(target_npc)

            last_tool_step = self._add_step(
                trace=trace,
                agent="Python Tool Runtime",
                action=f"Cast spell '{spell_result.get('spell_name')}'",
                details=spell_result,
                caused_by=s3.step_id
            )

        elif rules_analysis.get("action_type") == "resting":
            rest_type = rules_analysis.get("rest_type", "short")
            results = []
            for p in party:
                if rest_type == "long":
                    r = execute_long_rest(character=p)
                else:
                    r = execute_short_rest(character=p, hit_dice_to_spend=1, seed=seed)
                results.append(r)

            tool_calls_record.append({"tool": f"resting.execute_{rest_type}_rest", "output": results})
            self.state_manager.save_party(party)

            last_tool_step = self._add_step(
                trace=trace,
                agent="Python Tool Runtime",
                action=f"Execute {rest_type.capitalize()} Rest for Party",
                details={"rest_type": rest_type, "results": results},
                caused_by=s3.step_id
            )

        elif rules_analysis.get("action_type") == "ability_check":
            check_result = roll_check(
                character=actor,
                ability=rules_analysis.get("ability"),
                skill=rules_analysis.get("skill"),
                dc=rules_analysis.get("dc", 15),
                advantage=rules_analysis.get("advantage", False),
                disadvantage=rules_analysis.get("disadvantage", False),
                seed=seed
            )
            check_result["action_type"] = "ability_check"
            tool_calls_record.append({"tool": "mechanics.roll_check", "output": check_result})
            
            last_tool_step = self._add_step(
                trace=trace,
                agent="Python Tool Runtime",
                action=f"Execute deterministic d20 {check_result['check_type']} check",
                details={
                    "formula": check_result["formula"],
                    "total": check_result["total"],
                    "dc": check_result["dc"],
                    "success": check_result["success"],
                    "is_crit_20": check_result["is_crit_20"],
                },
                caused_by=s3.step_id
            )
            
        elif rules_analysis.get("action_type") == "combat_attack":
            target_npc = self.state_manager.get_npc(rules_analysis.get("target", "guard_karl")) or {
                "name": "Guard Karl", "ac": 14, "hp": {"current": 16, "max": 16}
            }
            attack_result = roll_attack(
                attacker=actor,
                target=target_npc,
                attack_name=rules_analysis.get("weapon"),
                seed=seed
            )
            tool_calls_record.append({"tool": "combat.roll_attack", "output": attack_result})
            
            last_tool_step = self._add_step(
                trace=trace,
                agent="Python Tool Runtime",
                action="Execute deterministic attack roll vs AC",
                details=attack_result,
                caused_by=s3.step_id
            )
            
            if attack_result["is_hit"]:
                damage_result = roll_damage(
                    attacker=actor,
                    target=target_npc,
                    damage_formula=attack_result.get("damage_formula", "1d6"),
                    damage_type=attack_result.get("damage_type", "piercing"),
                    is_critical=attack_result.get("is_critical_hit", False),
                    ability_bonus_key="dexterity",
                    seed=seed
                )
                apply_damage(target_npc, damage_result["final_damage"], damage_result["damage_type"])
                self.state_manager.update_npc(target_npc)
                tool_calls_record.append({"tool": "combat.roll_damage", "output": damage_result})
                
                last_tool_step = self._add_step(
                    trace=trace,
                    agent="Python Tool Runtime",
                    action=f"Calculate damage: {damage_result['final_damage']} {damage_result['damage_type']}",
                    details=damage_result,
                    caused_by=last_tool_step.step_id
                )
                
        # 5. NPC Agent -> Evaluate NPC Reactions
        primary_npc = self.state_manager.get_npc("guard_karl") or (npcs[0] if npcs else {})
        npc_reaction = self.npc_agent.evaluate_reaction(
            npc=primary_npc,
            player_action=intent,
            check_result=check_result,
            context=env_context
        )
        self._add_step(
            trace=trace,
            agent="NPC Agent",
            action=f"Simulate reaction and memory for {primary_npc.get('name', 'NPC')}",
            details=npc_reaction,
            caused_by=last_tool_step.step_id
        )
        
        # 6. Character Agent -> AI Companion Commentary
        companion = next((c for c in party if not c.get("is_player", True)), None)
        comp_reaction = None
        if companion:
            comp_reaction = self.character_agent.generate_companion_reaction(
                companion=companion,
                player_intent=intent,
                turn_result={"check": check_result, "attack": attack_result}
            )
            if comp_reaction:
                self._add_step(
                    trace=trace,
                    agent="Character Agent",
                    action=f"AI Companion {companion.get('name')} commentary / assistance",
                    details=comp_reaction,
                    caused_by=last_tool_step.step_id
                )
                
        # 7. State Mutations & Impact Analysis
        state_changes_summary = []
        proposed_state = self.state_manager.get_full_state()
        
        # If stealth was successful and player intended to steal key / unlock cell
        if check_result and check_result.get("success"):
            if "key" in intent.lower() and not world_state.get("global_flags", {}).get("dungeon_key_stolen"):
                world_state.setdefault("global_flags", {})["dungeon_key_stolen"] = True
                actor.setdefault("inventory", []).append("Fortress Iron Cell Key")
                self.state_manager.update_character(actor)
                self.state_manager.save_world(world_state)
                state_changes_summary.append("Acquired Fortress Iron Cell Key")
                
            if ("free" in intent.lower() or "valen" in intent.lower()) and not world_state.get("global_flags", {}).get("valen_freed"):
                world_state.setdefault("global_flags", {})["valen_freed"] = True
                valen = self.state_manager.get_npc("prisoner_valen")
                if valen:
                    valen["conditions"] = []
                    valen["disposition"] = "Liberated Companion"
                    self.state_manager.update_npc(valen)
                    
                quests = self.state_manager.get_quests()
                for q in quests:
                    if q.get("id") == "escape_the_fort":
                        for obj in q.get("objectives", []):
                            if obj.get("id") == "free_valen":
                                obj["completed"] = True
                self.state_manager.save_quests(quests)
                self.state_manager.save_world(world_state)
                state_changes_summary.append("Valen the Scholar liberated from Cell #3")
                
        proposed_state = self.state_manager.get_full_state()
        
        # 8. Impact Agent -> Check Consequential Threshold
        impact_report = self.impact_agent.evaluate_mutation(
            before_state=before_snapshot,
            proposed_state=proposed_state,
            cause=intent
        )
        
        impact_step = self._add_step(
            trace=trace,
            agent="Impact Agent",
            action="Assess consequential change impact & approval gate",
            details=impact_report.to_dict(),
            caused_by=last_tool_step.step_id
        )
        
        if impact_report.requires_approval:
            trace.requires_approval = True
            trace.approval_payload = impact_report.to_dict()
            trace.narration = f"[APPROVAL REQUIRED]: {impact_report.action}"
            return trace

        # 9. DM Agent -> Narration
        narration = self.dm_agent.narrate_turn(
            player_intent=intent,
            actor_name=actor.get("name", "Player"),
            world_context=env_context,
            check_result=check_result,
            attack_result=attack_result,
            damage_result=damage_result,
            npc_reaction=npc_reaction,
            companion_reaction=comp_reaction,
            state_changes_summary=state_changes_summary,
            spell_result=spell_result
        )
        trace.narration = narration
        
        dm_step = self._add_step(
            trace=trace,
            agent="DM Agent",
            action="Generate Theater-of-the-Mind narration",
            details={"narration_length": len(narration)},
            caused_by=impact_step.step_id
        )
        
        # 10. Commit turn to Git Versioning
        if auto_commit:
            commit_record = self.git_manager.commit(
                full_state=proposed_state,
                intent=intent,
                reason=narration[:100] + "...",
                agent="DM Agent",
                tool_calls=tool_calls_record,
                affected_files=["state/world.json", "state/party.json", "state/npcs.json"],
            )
            trace.commit_id = commit_record["commit_id"]
            
            self._add_step(
                trace=trace,
                agent="Git Versioning",
                action=f"Recorded commit snapshot `{commit_record['commit_id']}`",
                details=commit_record,
                caused_by=dm_step.step_id
            )
            
        return trace
