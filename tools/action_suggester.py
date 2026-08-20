"""
Dynamic Contextual Action Suggester for Agentic D&D.
Generates rich, tactical, and narrative RPG action suggestions tailored to
the active scene, current threats, actor abilities, and nearby NPCs.
No developer CLI commands or canned first-person scripts.
"""

from typing import Dict, Any, List, Optional
from tools.formatting import (
    BOLD, RESET, DIM, CYAN, GREEN, YELLOW, MAGENTA, RED,
    BRIGHT_YELLOW, BRIGHT_CYAN, BRIGHT_GREEN, BRIGHT_RED
)


class ActionSuggester:
    """
    Evaluates game context and generates contextual tactical & roleplay choices.
    """

    def generate_suggestions(
        self,
        actor: Dict[str, Any],
        scene: Dict[str, Any],
        threats: Optional[List[Any]] = None,
        npcs: Optional[List[Any]] = None,
        in_combat: bool = False
    ) -> Dict[str, List[Dict[str, str]]]:
        """
        Returns categorized action suggestions:
        {
          "combat": [...],
          "exploration": [...],
          "social": [...],
          "recovery": [...]
        }
        """
        suggestions: Dict[str, List[Dict[str, str]]] = {
            "combat": [],
            "exploration": [],
            "social": [],
            "recovery": []
        }

        actor_name = actor.get("name", "Hero")
        actor_class = actor.get("class", "Adventurer").lower()
        attacks = actor.get("attacks", [])
        cantrips = actor.get("cantrips", [])
        spells_prep = actor.get("spells_prepared", [])
        threat_list = threats or scene.get("threats", [])
        exits = scene.get("exits", [])
        npc_list = npcs or []

        # 1. Tactical Combat Options
        if threat_list or in_combat:
            target_str = threat_list[0] if threat_list else "enemy"
            if isinstance(target_str, dict):
                target_name = target_str.get("name", "Enemy")
            else:
                target_name = str(target_str).split("(")[0].strip()

            # Weapon attacks
            if attacks:
                for atk in attacks[:2]:
                    atk_name = atk.get("name", "Weapon")
                    dmg = atk.get("damage", "1d6")
                    dtype = atk.get("damage_type", "damage")
                    mastery = atk.get("mastery")
                    mastery_tag = f" [{mastery}]" if mastery else ""
                    suggestions["combat"].append({
                        "label": f"Strike with {atk_name}{mastery_tag}",
                        "desc": f"Engage {target_name} in melee (+{atk.get('bonus', 2)} to hit, {dmg} {dtype})"
                    })
            else:
                suggestions["combat"].append({
                    "label": "Melee Attack",
                    "desc": f"Strike {target_name} with your equipped weapon"
                })

            # Spells
            if cantrips or spells_prep:
                for sp in (cantrips + spells_prep)[:2]:
                    sp_title = sp.replace("_", " ").title()
                    suggestions["combat"].append({
                        "label": f"Cast {sp_title}",
                        "desc": f"Target {target_name} with magical attack / effect"
                    })

            # Defensive & Tactical
            suggestions["combat"].append({
                "label": "Seek Tactical Cover",
                "desc": "Move behind trees, wagons, or terrain (+2 to +5 AC bonus vs ranged attacks)"
            })
            suggestions["combat"].append({
                "label": "Dodge & Defensive Stance",
                "desc": "Focus entirely on defense; attacks against you have Disadvantage until next turn"
            })

        # 2. Exploration & Scouting Options
        scene_desc = scene.get("description", "").lower()
        if "horse" in scene_desc or "arrow" in scene_desc:
            suggestions["exploration"].append({
                "label": "Investigate Horse Carcasses",
                "desc": "Check saddlebags, arrow fletchings, and inspect for signs of an ambush"
            })
        if "trail" in scene_desc or "mud" in scene_desc or "thicket" in scene_desc:
            suggestions["exploration"].append({
                "label": "Track Footprints & Signs of Passage",
                "desc": "Examine the roadside mud to identify goblin numbers and travel direction"
            })
        if not suggestions["exploration"]:
            suggestions["exploration"].append({
                "label": "Search Immediate Surroundings",
                "desc": "Look for concealed paths, hidden loot, or secret compartments"
            })

        suggestions["exploration"].append({
            "label": "Stealth Reconnaissance",
            "desc": "Slip through cover to scout ahead without alerting nearby sentries"
        })

        if exits:
            for ex in exits[:2]:
                suggestions["exploration"].append({
                    "label": f"Advance: {ex.split()[0].title()} Path",
                    "desc": f"Move the party forward along: {ex}"
                })

        # 3. Social & Roleplay Options
        if npc_list:
            for n in npc_list[:2]:
                n_name = n.get("name", "NPC") if isinstance(n, dict) else str(n)
                suggestions["social"].append({
                    "label": f"Converse with {n_name}",
                    "desc": f"Inquire about local rumors, directions, or quest objectives"
                })
        elif threat_list:
            suggestions["social"].append({
                "label": "Demand Parley / Surrender",
                "desc": "Call out to the ambushers with an Intimidation or Persuasion check"
            })
        else:
            suggestions["social"].append({
                "label": "Party Consultation",
                "desc": "Discuss strategy and next steps with your adventuring companions"
            })

        # 4. Recovery & Party Options
        hp_info = actor.get("hp", {})
        cur_hp = hp_info.get("current", 10)
        max_hp = hp_info.get("max", 10)
        
        if cur_hp < max_hp:
            suggestions["recovery"].append({
                "label": "Short Rest & Bandage Wounds",
                "desc": f"Spend Hit Dice to recover HP (Current: {cur_hp}/{max_hp} HP)"
            })
        else:
            suggestions["recovery"].append({
                "label": "Short Rest",
                "desc": "Take a 1-hour rest to recharge short-rest class abilities"
            })

        suggestions["recovery"].append({
            "label": "Long Rest / Make Camp",
            "desc": "Establish a secure camp for 8 hours; full HP and spell slot restoration"
        })

        return suggestions

    def render_action_panel(
        self,
        actor: Dict[str, Any],
        scene: Dict[str, Any],
        threats: Optional[List[Any]] = None,
        npcs: Optional[List[Any]] = None,
        in_combat: bool = False
    ) -> str:
        """
        Renders an elegant, non-developer visual action suggestion panel.
        """
        data = self.generate_suggestions(actor, scene, threats, npcs, in_combat)
        lines = []

        # If threats or combat, show Combat first
        if threat_list := (threats or scene.get("threats")):
            lines.append(f"  {BRIGHT_RED}⚔️ TACTICAL COMBAT OPTIONS:{RESET}")
            for item in data["combat"][:3]:
                lines.append(f"    • {BOLD}{item['label']}{RESET} — {DIM}{item['desc']}{RESET}")

        lines.append(f"\n  {BRIGHT_CYAN}🔍 EXPLORATION & ENVIRONMENT:{RESET}")
        for item in data["exploration"][:3]:
            lines.append(f"    • {BOLD}{item['label']}{RESET} — {DIM}{item['desc']}{RESET}")

        if data["social"]:
            lines.append(f"\n  {BRIGHT_YELLOW}🗣️ SOCIAL & INTERACTION:{RESET}")
            for item in data["social"][:2]:
                lines.append(f"    • {BOLD}{item['label']}{RESET} — {DIM}{item['desc']}{RESET}")

        lines.append(f"\n  {BRIGHT_GREEN}⛺ RECOVERY & PREPARATION:{RESET}")
        for item in data["recovery"][:2]:
            lines.append(f"    • {BOLD}{item['label']}{RESET} — {DIM}{item['desc']}{RESET}")

        return "\n".join(lines)
