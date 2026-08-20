#!/usr/bin/env python3
"""
Agentic D&D CLI Router & Agent Bridge.
Provides slash-command execution, programmatic JSON APIs, and terminal workflows
for Antigravity, Claude Code, Codex, and human players.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Optional, List, Dict, Any

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agents.orchestrator import OrchestratorAgent
from agents.developer import DeveloperAgent
from tools.state_manager import StateManager
from tools.git_versioning import CampaignGitManager
from tools.dice import roll_dice
from tools.mechanics import roll_check, roll_saving_throw
from tools.combat import roll_attack, roll_damage, apply_damage, apply_healing
from tools.permissions import RuntimeMode, PermissionManager
from tools.encounters import calculate_encounter_difficulty, get_xp_by_cr, get_adventuring_day_budget
from tools.monsters import get_monster, load_monsters
from tools.magic_items import get_magic_item, load_magic_items
from tools.spells import cast_spell, get_spell, load_spells
from tools.resting import execute_short_rest, execute_long_rest
from tools.death_saves import roll_death_save, stabilize_character
from tools.adventure_loader import AdventureLoader
from tools.character_creator import CharacterCreator, LMOP_PRESETS
from tools.character_inspector import CharacterInspector
from tools.multiplayer import MultiplayerManager
from tools.level_up import LevelUpManager
from tools.formatting import (
    render_hp_bar, render_slot_pips, box_header, box_section,
    badge, format_dm_narration, format_dialogue,
    BOLD, RESET, DIM, ITALIC, CYAN, GREEN, YELLOW, RED, BLUE, MAGENTA, WHITE,
    BRIGHT_YELLOW, BRIGHT_CYAN, BRIGHT_GREEN, BRIGHT_RED, BRIGHT_BLUE, BRIGHT_MAGENTA
)


def get_managers():
    sm = StateManager(str(PROJECT_ROOT))
    git = CampaignGitManager(str(PROJECT_ROOT))
    orch = OrchestratorAgent(str(PROJECT_ROOT))
    dev = DeveloperAgent(str(PROJECT_ROOT))
    return sm, git, orch, dev


def cmd_play(args):
    """Processes natural language player intent through the multi-agent orchestrator."""
    sm, _, orch, _ = get_managers()
    intent = " ".join(args.intent)
    trace = orch.process_player_intent(
        intent=intent,
        character_id=args.character,
        seed=args.seed,
        auto_commit=not args.no_commit
    )

    if args.json:
        print(json.dumps(trace.to_dict(), indent=2))
        return

    print("\n" + box_header(f"PLAYER ACTION: > {intent}", width=70, color=BRIGHT_CYAN))

    print(box_section("Autonomous Multi-Agent Execution Trace", color=YELLOW))
    for step in trace.steps:
        agent = step.agent
        formula_str = f" {DIM}({step.details['formula']}){RESET}" if "formula" in step.details else ""
        print(f"  {CYAN}▶{RESET} [{BOLD}{agent}{RESET}] {step.action}{formula_str}")

    if trace.requires_approval and trace.approval_payload:
        print("\n" + box_header("CONSEQUENTIAL CHANGE DETECTED — APPROVAL REQUIRED", width=70, color=BRIGHT_RED))
        print(f"  Action: {trace.approval_payload.get('action')}")
        print(f"  Cause:  {trace.approval_payload.get('cause')}")
        print(f"  Affected: {', '.join(trace.approval_payload.get('affected_files', []))}")
        print("\n  To approve or reject, run:")
        print("    python dnd.py approve --decision approve")
        print("    python dnd.py approve --decision reject")
        return

    print(box_section("DM Narration & Scene Atmosphere", color=BRIGHT_MAGENTA))
    print(format_dm_narration(trace.narration))

    # In-Turn Mini HUD
    from tools.formatting import render_turn_mini_hud
    mp = MultiplayerManager(str(PROJECT_ROOT))
    active_char = mp.get_active_player() or (sm.get_party()[0] if sm.get_party() else {})
    print("\n" + render_turn_mini_hud(actor=active_char, world_state=sm.get_world()))

    if trace.commit_id:
        print(f"  {DIM}[Snapshot Commit: {trace.commit_id}]{RESET}")
    print("=" * 70 + "\n")


def cmd_status(args):
    """Displays party stats, current scene, environment, threats, and quests."""
    sm, _, _, _ = get_managers()
    world = sm.get_world()
    party = sm.get_party()
    npcs = sm.get_npcs()
    quests = sm.get_quests()
    mp = MultiplayerManager(str(PROJECT_ROOT))
    active_player = mp.get_active_player()
    active_id = active_player.get("id") if active_player else None

    if args.json:
        print(json.dumps(sm.get_full_state(), indent=2))
        return

    title_str = f"{world.get('campaign_name', 'Agentic D&D')} — Status"
    print("\n" + box_header(title_str, width=70, color=BRIGHT_CYAN))
    print(f"  {BOLD}Location:{RESET} {world.get('active_location')} | {BOLD}Time:{RESET} {world.get('time_of_day')} | {BOLD}Weather:{RESET} {world.get('weather')}")
    print(f"  {BOLD}Lighting:{RESET} {world.get('lighting')} | {BOLD}Tension:{RESET} {world.get('tension_level')}")

    scene = world.get("current_scene", {})
    if scene:
        print(box_section(f"SCENE: {scene.get('title', 'Current Area')}", color=CYAN))
        print(f"  {scene.get('description', '')}")
        if scene.get("threats"):
            print(f"\n  {BRIGHT_RED}Active Threats / Obstacles:{RESET}")
            for t in scene["threats"]:
                print(f"   • {t}")
        if scene.get("exits"):
            print(f"\n  {GREEN}Exits & Connections:{RESET}")
            for e in scene["exits"]:
                print(f"   • {e}")

    print(box_section("PARTY ROSTER", color=BRIGHT_YELLOW))
    for p in party:
        hp = p.get("hp", {})
        conds = ", ".join(p.get("conditions", [])) if p.get("conditions") else "None"
        ctrl = "Player" if p.get("is_player", True) else "AI Companion"
        is_active = p.get("id") == active_id
        active_badge = f" {badge('ACTIVE', 'active')}" if is_active else ""
        
        hp_bar = render_hp_bar(hp.get("current", 10), hp.get("max", 10), hp.get("temp", 0))
        print(f"  * {BOLD}{p.get('name')}{RESET} (Lvl {p.get('level', 1)} {p.get('class', '')} [{ctrl}]){active_badge}")
        print(f"    Health:    {hp_bar} | AC: {BOLD}{p.get('ac')}{RESET} | Conditions: {conds}")
        if "hit_dice" in p:
            hd = p["hit_dice"]
            print(f"    Hit Dice:  {hd.get('current')}/{hd.get('max')} ({hd.get('die', '1d8')})")
        if "spell_slots" in p:
            slot_strs = [f"Lvl {k.split('_')[1]}: {render_slot_pips(v.get('current', 0), v.get('max', 0))}" for k, v in p["spell_slots"].items()]
            print(f"    Spell Slots: {' | '.join(slot_strs)}")

    if npcs:
        print(box_section("NPCS IN AREA", color=YELLOW))
        for n in npcs:
            hp = n.get("hp", {})
            hp_str = f" [HP: {hp.get('current')}/{hp.get('max')}]" if hp else ""
            disp = n.get("disposition", 0)
            disp_color = GREEN if disp > 20 else (RED if disp < -20 else YELLOW)
            disp_str = f"{disp_color}{disp:+d}{RESET}"
            print(f"  • {BOLD}{n.get('name')}{RESET} ({n.get('role')}) - Status: {n.get('status', 'Alive')}{hp_str} | Disposition: {disp_str}")

    if quests:
        print(box_section("ACTIVE QUESTS", color=BRIGHT_GREEN))
        for q in quests:
            prio = q.get("priority", "Normal")
            print(f"  • {BOLD}{q.get('title')}{RESET} [{badge(q.get('status', 'active'), 'info')}] (Priority: {prio}):")
            for obj in q.get("objectives", []):
                mark = f"{GREEN}[✓]{RESET}" if obj.get("completed") else f"{DIM}[ ]{RESET}"
                print(f"     {mark} {obj.get('description')}")
    print("\n" + "=" * 70 + "\n")


def cmd_roll(args):
    """Rolls tabletop dice deterministically."""
    res = roll_dice(
        expression=args.expression,
        advantage=args.adv,
        disadvantage=args.disadv,
        is_critical=args.crit,
        bonus=args.bonus,
        seed=args.seed
    )
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"Dice Roll: {args.expression}")
        print(f"Formula:   {res['formula']}")
        print(f"Total:     {res['total']}")
        if res.get("is_crit_20"):
            print("CRITICAL HIT! (Natural 20)")
        elif res.get("is_crit_1"):
            print("CRITICAL FUMBLE! (Natural 1)")


def cmd_check(args):
    """Executes a D&D 2024 ability or skill check."""
    sm, _, _, _ = get_managers()
    char = sm.get_character(args.character) if args.character else (sm.get_party()[0] if sm.get_party() else {})
    if not char:
        print(f"Error: Character '{args.character}' not found.", file=sys.stderr)
        sys.exit(1)

    from tools.suggestions import suggest_skill
    known_skills_abilities = [
        "athletics", "acrobatics", "sleight_of_hand", "stealth", "arcana", "history",
        "investigation", "nature", "religion", "animal_handling", "insight", "medicine",
        "perception", "survival", "deception", "intimidation", "performance", "persuasion",
        "strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"
    ]
    clean_skill = args.skill.lower().replace(" ", "_")
    if clean_skill not in known_skills_abilities:
        suggs = suggest_skill(args.skill)
        print(f"\n{YELLOW}[! Note: '{args.skill}' is not a standard 5e skill. Did you mean: {', '.join(suggs)}?]{RESET}")

    res = roll_check(
        character=char,
        skill=args.skill,
        dc=args.dc,
        advantage=args.adv,
        disadvantage=args.disadv,
        guidance=args.guidance,
        extra_bonus=args.bonus,
        seed=args.seed
    )
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        status_text = "SUCCESS" if res["success"] else "FAILURE"
        print(f"\n{char.get('name')} {args.skill.capitalize()} Check vs DC {res['dc']}:")
        print(f"Outcome: {status_text} (Total: {res['total']})")
        print(f"Formula: {res['formula']}")
        print(f"Proficient: {res['is_proficient']} | Expertise: {res['has_expertise']}")


def cmd_attack(args):
    """Executes a weapon attack and damage roll against target AC."""
    sm, _, _, _ = get_managers()
    attacker = sm.get_character(args.attacker) if args.attacker else (sm.get_party()[0] if sm.get_party() else {})
    target = sm.get_npc(args.target) or {"name": args.target, "ac": args.ac or 14, "hp": {"current": 20, "max": 20}}

    atk_res = roll_attack(
        attacker=attacker,
        target=target,
        attack_name=args.weapon,
        advantage=args.adv,
        disadvantage=args.disadv,
        cover=getattr(args, "cover", "none"),
        extra_bonus=args.bonus,
        seed=args.seed
    )

    dmg_res = None
    applied = None
    if atk_res.get("is_hit"):
        dmg_res = roll_damage(
            attacker=attacker,
            target=target,
            damage_formula=atk_res.get("damage_formula", "1d6"),
            damage_type=atk_res.get("damage_type", "slashing"),
            is_critical=atk_res.get("is_critical_hit", False),
            seed=args.seed
        )
        if isinstance(target, dict) and "hp" in target:
            applied = apply_damage(target, dmg_res["final_damage"], dmg_res["damage_type"])
            if sm.get_npc(args.target):
                sm.update_npc(target)

    payload = {
        "attack": atk_res,
        "damage": dmg_res,
        "applied": applied
    }

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"\n{attacker.get('name')} attacks {target.get('name')} with {atk_res.get('attack_name')}:")
        cov_str = f" [Cover: {args.cover}]" if getattr(args, "cover", "none") != "none" else ""
        print(f"Attack Roll: {atk_res['formula']} vs AC {atk_res['target_ac']}{cov_str} -> {'HIT!' if atk_res.get('is_hit') else 'MISS'}")
        if dmg_res:
            print(f"Damage:      {dmg_res['formula']} ({dmg_res['damage_type']}) -> {dmg_res['final_damage']} dmg")
            if applied:
                print(f"Target HP:   {applied['hp_before']} -> {applied['hp_after']}/{applied['max_hp']}")


def cmd_rest(args):
    """Executes a Short or Long Rest for party members."""
    sm, _, _, _ = get_managers()
    party = sm.get_party()
    
    if args.character:
        chars = [c for c in party if c.get("id") == args.character or c.get("name").lower() == args.character.lower()]
    else:
        chars = party

    if not chars:
        print("No characters found to rest.", file=sys.stderr)
        sys.exit(1)

    results = []
    for c in chars:
        if args.type == "short":
            res = execute_short_rest(c, hit_dice_to_spend=args.hit_dice, seed=args.seed)
        else:
            res = execute_long_rest(c)
        sm.update_character(c)
        results.append(res)

    if args.json:
        print(json.dumps(results, indent=2))
        return

    print("\n" + "=" * 65)
    print(f"PARTY REST COMPLETE: [{args.type.upper()} REST]")
    print("=" * 65)
    for r in results:
        if args.type == "short":
            print(f"* {r['character']}: Regained {r['hp_healed']} HP (Spent {r['hit_dice_spent']} HD) -> HP: {r['hp_after']}/{r['max_hp']} [HD Remaining: {r['hit_dice_remaining']}]")
        else:
            print(f"* {r['character']}: Fully restored to {r['hp_after']} HP | Recovered {r['hit_dice_recovered']} HD ({r['hit_dice_current']}/{r['hit_dice_max']}) | Spell slots & abilities reset!")
    print("=" * 65 + "\n")


def cmd_cast(args):
    """Casts a spell from the Player's Handbook compendium."""
    sm, _, _, _ = get_managers()
    caster = sm.get_character(args.character) if args.character else (sm.get_party()[0] if sm.get_party() else {})
    target = sm.get_npc(args.target) if args.target else None
    if not target and args.target:
        target = sm.get_character(args.target)

    res = cast_spell(
        caster=caster,
        spell_name=args.spell,
        target=target,
        slot_level=args.level,
        is_ritual=args.ritual,
        seed=args.seed
    )

    if not res.get("success"):
        print(f"Cast Error: {res.get('error')}", file=sys.stderr)
        sys.exit(1)

    sm.update_character(caster)
    if target:
        if sm.get_npc(args.target):
            sm.update_npc(target)
        elif sm.get_character(args.target):
            sm.update_character(target)

    if args.json:
        print(json.dumps(res, indent=2))
        return

    print("\n" + "=" * 65)
    rit_str = " (Ritual - 0 slots)" if res.get("is_ritual") else (f" (Level {res['level_cast']} Slot)" if res['level_cast'] > 0 else " (Cantrip)")
    print(f"{res['caster'].upper()} CASTS {res['spell'].upper()}{rit_str}")
    print("=" * 65)
    if "damage" in res:
        print(f"Damage: {res['formula']} ({res['damage_type']}) -> {res['damage']} damage to {res.get('target_name')}")
        if "target_hp_after" in res:
            print(f"Target HP: {res['target_hp_after']}")
    elif "healing" in res:
        print(f"Healing: {res['formula']} -> Regained {res['healing']} HP for {res.get('target_name')}")
        if "target_hp_after" in res:
            print(f"Target HP: {res['target_hp_after']}")
    elif "total_damage" in res:
        print(f"Magic Missile: {res['darts_count']} darts dealing {res['dart_damages']} = {res['total_damage']} force damage to {res.get('target_name')}")
    else:
        print(f"Spell Manifests: Duration {res['duration']}")
    if res.get("concentration"):
        print(f"[Maintaining Active Concentration on {res['spell']}]")
    print("=" * 65 + "\n")


def cmd_spell(args):
    """Displays a spell card from the Player's Handbook."""
    sp = get_spell(args.name)
    if not sp:
        from tools.suggestions import suggest_spell
        suggs = suggest_spell(args.name)
        print(f"Spell '{args.name}' not found. Did you mean: {', '.join(suggs)}?", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(sp, indent=2))
        return

    print("\n" + "=" * 65)
    lvl_str = "Cantrip" if sp["level"] == 0 else f"{sp['level']}th Level"
    rit = " (Ritual)" if sp.get("ritual") else ""
    print(f"{sp['name'].upper()} [{lvl_str} {sp['school']}{rit}]")
    print("=" * 65)
    print(f"Casting Time: {sp['casting_time']} | Range: {sp['range']}")
    print(f"Components:   {', '.join(sp['components'])} | Duration: {sp['duration']}")
    print("\n" + sp["description"])
    if sp.get("upcasting"):
        print(f"\n* At Higher Levels: {sp['upcasting']}")
    print("=" * 65 + "\n")


def cmd_death_save(args):
    """Rolls a Death Saving Throw for a character at 0 HP."""
    sm, _, _, _ = get_managers()
    char = sm.get_character(args.character) if args.character else (sm.get_party()[0] if sm.get_party() else {})
    res = roll_death_save(char, seed=args.seed)
    
    if not res.get("success", True):
        print(f"Death Save Error: {res.get('error')}", file=sys.stderr)
        sys.exit(1)

    sm.update_character(char)

    if args.json:
        print(json.dumps(res, indent=2))
        return

    print("\n" + "=" * 65)
    print(f"DEATH SAVING THROW — {res.get('character', 'Character')}")
    print("=" * 65)
    print(f"D20 Roll: {res.get('roll')} -> {res.get('result_type')}")
    print(f"Progress: {res.get('successes')}/3 Successes | {res.get('failures')}/3 Failures")
    print(f"STATUS:   [{res.get('status').upper()}]")
    if res.get("hp_regained", 0) > 0:
        print("A spark of divine vigor surges through you! You regain 1 HP and open your eyes!")
    print("=" * 65 + "\n")


def cmd_stabilize(args):
    """Attempts to stabilize an unconscious ally with a DC 10 Medicine check."""
    sm, _, _, _ = get_managers()
    party = sm.get_party()
    healer = sm.get_character(args.healer) if args.healer else party[0]
    target = sm.get_character(args.target) or (party[1] if len(party) > 1 else party[0])

    res = stabilize_character(healer, target, seed=args.seed)
    if res["success"]:
        sm.update_character(target)

    if args.json:
        print(json.dumps(res, indent=2))
        return

    print("\n" + "=" * 65)
    print(f"STABILIZATION ATTEMPT")
    print("=" * 65)
    chk = res["check"]
    print(f"{healer.get('name')} Medicine Check: {chk['formula']} vs DC 10 -> {'SUCCESS' if chk['success'] else 'FAILURE'}")
    print(f"{res['message']}")
    print("=" * 65 + "\n")


def cmd_history(args):
    """Displays the Git-style commit timeline."""
    _, git, _, _ = get_managers()
    timeline = git.get_history_timeline(args.branch)
    if args.json:
        print(json.dumps(timeline, indent=2))
    else:
        print("\n=== Git-Style Campaign Timeline ===")
        for c in timeline[:args.limit]:
            print(f"Commit [{c['commit_id']}] ({c['timestamp']}) | {c['agent']}")
            print(f"  Intent: > {c['intent']}")
            print(f"  Reason: {c['reason']}")
            print(f"  Files:  {', '.join(c.get('affected_files', []))}")
            print("-" * 50)
        print()


def cmd_diff(args):
    """Calculates unified state diff between commits."""
    _, git, _, _ = get_managers()
    diff = git.compute_diff(args.commit_a, args.commit_b)
    if args.json:
        print(json.dumps(diff, indent=2))
    else:
        from tools.formatting import render_state_diff
        print("\n" + render_state_diff(diff.get("diffs", {})))


def cmd_rollback(args):
    """Restores the campaign and markdown files to a specific snapshot commit."""
    _, git, _, _ = get_managers()
    res = git.rollback(args.commit_id)
    if res:
        print(f"Successfully rolled back campaign state to snapshot commit '{args.commit_id}'.")
    else:
        print(f"Error: Commit '{args.commit_id}' not found.", file=sys.stderr)
        sys.exit(1)


def cmd_branch(args):
    """Creates or switches campaign timeline branch."""
    _, git, _, _ = get_managers()
    if args.create:
        ok = git.create_branch(args.branch_name)
        if ok:
            print(f"Created and switched to timeline branch '{args.branch_name}'.")
        else:
            print(f"Error: Branch '{args.branch_name}' already exists.", file=sys.stderr)
    else:
        res = git.switch_branch(args.branch_name)
        if res is not None:
            print(f"Switched to timeline branch '{args.branch_name}'.")
        else:
            print(f"Error: Branch '{args.branch_name}' not found.", file=sys.stderr)


def cmd_encounter(args):
    """Calculates encounter difficulty according to D&D Basic Rules."""
    sm, _, _, _ = get_managers()
    party_levels = []
    if args.party:
        party_levels = [int(x.strip()) for x in args.party.split(",") if x.strip()]
    else:
        party = sm.get_party()
        party_levels = [p.get("level", 1) for p in party] if party else [1, 1, 1, 1]

    if getattr(args, "preset", None):
        from tools.encounters import evaluate_preset_encounter
        res = evaluate_preset_encounter(
            preset_id=args.preset,
            party_levels=party_levels,
            situational_modifier=args.situational
        )
        if not res.get("success"):
            print(f"Error: {res.get('error')} Available: {', '.join(res.get('available_presets', []))}", file=sys.stderr)
            sys.exit(1)
        if args.json:
            print(json.dumps(res, indent=2))
            return
        print("\n" + "=" * 65)
        print(f"PRESET ENCOUNTER: {res.get('preset_name', args.preset).upper()}")
        print("=" * 65)
        print(f"Party: {len(party_levels)} Adventurers (Levels: {', '.join(map(str, party_levels))})")
        print(f"Monsters: {', '.join(res['monsters_breakdown'])}")
        print(f"Base XP: {res['base_xp']} XP | Multiplier: x{res['multiplier']} -> Adjusted XP: {res['adjusted_xp']} XP")
        print(f"DIFFICULTY: [{res['difficulty'].upper()}]")
        if res.get("tactics"):
            print(f"\nTactics: {res['tactics']}")
        print(f"Adventuring Day Impact: {res['adventuring_day_percent']}% of daily budget")
        print("=" * 65 + "\n")
        return

    monster_xps = []
    monster_names = []
    if args.monsters:
        for entry in args.monsters.split(","):
            entry = entry.strip()
            if not entry:
                continue
            parts = entry.split(":")
            m_id = parts[0].strip()
            count = int(parts[1]) if len(parts) > 1 else 1
            
            # Check if monster is known in bestiary
            m_stat = get_monster(m_id)
            if m_stat:
                xp = m_stat.get("xp", 50)
                name = m_stat.get("name", m_id)
            elif m_id.startswith("cr"):
                cr_val = m_id[2:]
                xp = get_xp_by_cr(cr_val)
                name = f"CR {cr_val} Creature"
            elif m_id.isdigit():
                xp = int(m_id)
                name = f"{xp} XP Creature"
            else:
                xp = 50
                name = m_id.capitalize()

            for _ in range(count):
                monster_xps.append(xp)
            monster_names.append(f"{count}x {name} ({xp} XP each)")

    result = calculate_encounter_difficulty(
        party_levels=party_levels,
        monster_xps=monster_xps,
        situational_modifier=args.situational
    )
    result["monsters_breakdown"] = monster_names

    if args.json:
        print(json.dumps(result, indent=2))
        return

    print("\n" + "=" * 65)
    print("D&D BASIC RULES — ENCOUNTER DIFFICULTY EVALUATION")
    print("=" * 65)
    print(f"Party: {len(party_levels)} Adventurers (Levels: {', '.join(map(str, party_levels))})")
    print(f"Party Thresholds: Easy={result['party_thresholds']['easy']} | Medium={result['party_thresholds']['medium']} | Hard={result['party_thresholds']['hard']} | Deadly={result['party_thresholds']['deadly']} XP")
    print(f"Monsters: {', '.join(monster_names) if monster_names else 'None'}")
    print(f"Base Monster XP: {result['base_xp']} XP | Multiplier: x{result['multiplier']} -> Adjusted XP: {result['adjusted_xp']} XP")
    print(f"DIFFICULTY: [{result['difficulty'].upper()}]" + (f" (Situational mod: {args.situational})" if args.situational else ""))
    print(f"Adventuring Day Impact: {result['adventuring_day_percent']}% of daily budget ({result['adventuring_day_budget']} XP)")
    print("=" * 65 + "\n")


def cmd_monster(args):
    """Displays monster statblock from D&D Basic Rules or active adventure."""
    m = get_monster(args.name)
    if not m:
        print(f"Monster '{args.name}' not found in bestiary. Available: {', '.join(load_monsters().keys())}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(m, indent=2))
        return

    print("\n" + "=" * 65)
    source_str = f" [{m['_source']}]" if "_source" in m else ""
    print(f"{m.get('name').upper()}{source_str} ({m.get('size')} {m.get('type')}, {m.get('alignment')})")
    print("=" * 65)
    print(f"Armor Class: {m.get('ac')} ({m.get('armor_type', 'natural armor')})")
    hp = m.get("hp", {})
    print(f"Hit Points:  {hp.get('current')}/{hp.get('max')} ({hp.get('formula', '')})")
    print(f"Speed:       {m.get('speed')} ft." + (f", fly {m.get('fly_speed')} ft." if m.get("fly_speed") else ""))
    stats = m.get("stats", {})
    print(f"STR:{stats.get('strength')} DEX:{stats.get('dexterity')} CON:{stats.get('constitution')} INT:{stats.get('intelligence')} WIS:{stats.get('wisdom')} CHA:{stats.get('charisma')}")
    print(f"Challenge:   {m.get('cr')} ({m.get('xp')} XP) | Senses: {m.get('senses')}")
    if m.get("traits"):
        print("\n--- Special Traits ---")
        for t_name, t_desc in m["traits"].items():
            print(f"* {t_name.replace('_', ' ').title()}: {t_desc}")
    if m.get("actions"):
        print("\n--- Actions ---")
        for a in m["actions"]:
            dmg = f" -> {a.get('damage')} {a.get('damage_type')}" if a.get("damage") else ""
            print(f"* {a.get('name')}: +{a.get('bonus', 0)} to hit{dmg} {a.get('description', '')}")
    if m.get("legendary_actions"):
        print("\n--- Legendary Actions ---")
        for la in m["legendary_actions"]:
            print(f"* {la.get('name')} (Cost: {la.get('cost', 1)}): {la.get('description')}")
    print("=" * 65 + "\n")


def cmd_item(args):
    """Displays magic item information from D&D Basic Rules or active adventure."""
    it = get_magic_item(args.name)
    if not it:
        print(f"Magic item '{args.name}' not found. Available: {', '.join(load_magic_items().keys())}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(it, indent=2))
        return

    print("\n" + "=" * 65)
    attune = " (Requires Attunement)" if it.get("attunement") else ""
    source_str = f" [{it['_source']}]" if "_source" in it else ""
    print(f"{it.get('name').upper()}{source_str} [{it.get('type')}, {it.get('rarity')}{attune}]")
    print("=" * 65)
    print(it.get("description", ""))
    if it.get("bonuses"):
        print(f"Bonuses: {it['bonuses']}")
    if it.get("charges"):
        print(f"Charges: {it['charges']}")
    print("=" * 65 + "\n")


def cmd_test(args):
    """Runs the automated test suite."""
    _, _, _, dev = get_managers()
    res = dev.run_tests(args.pattern)
    print(res["output"])
    if not res["passed"]:
        sys.exit(1)


def cmd_adventure(args):
    """Manages modular adventure packages (list, info, load)."""
    loader = AdventureLoader()
    if args.action == "list":
        advs = loader.list_adventures()
        if args.json:
            print(json.dumps(advs, indent=2))
            return
        print("\n=== Available Adventure Modules ===")
        for a in advs:
            lvl = a.get("recommended_levels", {})
            lvl_str = f"Levels {lvl.get('start', 1)}-{lvl.get('end', 5)}" if lvl else "All Levels"
            print(f"* [{a.get('id')}] {a.get('title')} ({lvl_str})")
            if a.get("setting"):
                print(f"  Setting: {a.get('setting')} | Author: {a.get('author')}")
        print()
    elif args.action == "info":
        if not args.adventure_id:
            print("Error: Specify adventure ID (e.g. 'lost_mine_of_phandelver').", file=sys.stderr)
            sys.exit(1)
        adv = loader.get_adventure(args.adventure_id)
        if not adv:
            print(f"Error: Adventure '{args.adventure_id}' not found.", file=sys.stderr)
            sys.exit(1)
        val = loader.validate_adventure(args.adventure_id)
        if args.json:
            print(json.dumps({"manifest": adv, "validation": val}, indent=2))
            return
        print(f"\nADVENTURE: {adv.get('title').upper()} [{adv.get('id')}]")
        print("=" * 60)
        print(f"Setting: {adv.get('setting')} | Levels: {adv.get('recommended_levels')}")
        print(f"Starting Scene: {adv.get('starting_scene', {}).get('title')}")
        print(f"\nChapters:")
        for ch in adv.get("chapters", []):
            print(f" - {ch.get('title')} ({ch.get('file')})")
        print(f"\nIntegrity: {'VALID' if val['valid'] else 'INVALID'}")
        print()
    elif args.action == "load":
        if not args.adventure_id:
            print("Error: Specify adventure ID to load (e.g. 'lost_mine_of_phandelver').", file=sys.stderr)
            sys.exit(1)
        res = loader.load_adventure_into_campaign(args.adventure_id)
        if args.json:
            print(json.dumps(res, indent=2))
            return
        print(f"\n{GREEN}✓ {res['message']}{RESET}\n")
    elif args.action == "new" or args.action == "scaffold":
        if not args.adventure_id:
            print("Error: Specify adventure slug to create (e.g. 'curse_of_strahd').", file=sys.stderr)
            sys.exit(1)
        title = getattr(args, "title", None)
        levels = getattr(args, "levels", "1-5")
        res = loader.scaffold_adventure(slug=args.adventure_id, title=title, recommended_levels=levels)
        if getattr(args, "json", False):
            print(json.dumps(res, indent=2))
            return
        if res["success"]:
            print(f"\n{GREEN}✓ {res['message']}{RESET}\n")
        else:
            print(f"\n{RED}✗ Error: {res['error']}{RESET}\n", file=sys.stderr)
            sys.exit(1)


def cmd_create_character(args):
    """Creates a new D&D 5e character and saves to party."""
    creator = CharacterCreator(str(PROJECT_ROOT))
    inspector = CharacterInspector(str(PROJECT_ROOT))
    mp = MultiplayerManager(str(PROJECT_ROOT))

    name = getattr(args, "name", None)
    char_class = getattr(args, "char_class", "Fighter")
    species = getattr(args, "species", "Human")
    background = getattr(args, "background", "Soldier")
    method = getattr(args, "method", "standard")
    preset = getattr(args, "preset", None)

    if getattr(args, "interactive", False):
        print("\n" + box_header("INTERACTIVE D&D 5E CHARACTER CREATOR", width=70, color=BRIGHT_CYAN))
        print("Welcome, Adventurer! Let's forge your legend step-by-step.\n")
        try:
            name_in = input("Enter Character Name [Valeros]: ").strip()
            name = name_in if name_in else "Valeros"

            print("\nClasses: Fighter, Wizard, Rogue, Cleric, Paladin, Barbarian, Ranger, Druid, Monk, Bard, Sorcerer, Warlock")
            cls_in = input("Choose Class [Fighter]: ").strip()
            char_class = cls_in if cls_in else "Fighter"

            print("\nSpecies: Human, Variant Human, High Elf, Wood Elf, Drow, Hill Dwarf, Mountain Dwarf, Lightfoot Halfling, Stout Halfling, Dragonborn, Forest Gnome, Rock Gnome, Half-Elf, Half-Orc, Tiefling")
            spc_in = input("Choose Species [Human]: ").strip()
            species = spc_in if spc_in else "Human"

            print("\nBackgrounds: Soldier, Criminal, Sage, Acolyte, Folk Hero, Noble, Outlander, Urchin")
            bg_in = input("Choose Background [Soldier]: ").strip()
            background = bg_in if bg_in else "Soldier"

            print("\nScore Generation: standard (15,14,13,12,10,8) | roll (4d6 drop lowest)")
            m_in = input("Choose Method [standard]: ").strip()
            method = m_in if m_in else "standard"
        except (EOFError, KeyboardInterrupt):
            pass

    if preset and not name:
        name = LMOP_PRESETS.get(preset, {}).get("name", "Hero")

    if not name:
        name = "Hero"

    custom_scores = None
    if getattr(args, "scores", None):
        parts = [int(x.strip()) for x in args.scores.split(",") if x.strip()]
        if len(parts) == 6:
            custom_scores = {
                "strength": parts[0], "dexterity": parts[1], "constitution": parts[2],
                "intelligence": parts[3], "wisdom": parts[4], "charisma": parts[5]
            }

    char = creator.create_character(
        name=name,
        char_class=char_class,
        species=species,
        background=background,
        method=method,
        custom_scores=custom_scores,
        is_player=not getattr(args, "companion", False),
        preset=preset,
        seed=getattr(args, "seed", None)
    )

    if getattr(args, "activate", False):
        mp.set_active_player(char["id"])

    if args.json:
        print(json.dumps(char, indent=2))
        return

    print("\n" + box_header("CHARACTER CREATION COMPLETE!", width=70, color=BRIGHT_GREEN))
    print(inspector.render_character_sheet(char))


def cmd_level_up(args):
    """Levels up a character from level L to L+1."""
    lum = LevelUpManager(str(PROJECT_ROOT))
    inspector = CharacterInspector(str(PROJECT_ROOT))
    mp = MultiplayerManager(str(PROJECT_ROOT))

    char_target = args.character
    if not char_target:
        active = mp.get_active_player()
        char_target = active.get("id") if active else None

    if not char_target:
        print("Error: Specify character ID or name to level up.", file=sys.stderr)
        sys.exit(1)

    hp_choice = "roll" if getattr(args, "roll", False) else "average"
    res = lum.level_up_character(char_target, hp_choice=hp_choice, seed=getattr(args, "seed", None))

    if not res["success"]:
        print(f"Error: {res['error']}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(res, indent=2))
        return

    char = res["character"]
    print("\n" + box_header(f"LEVEL UP COMPLETE — {char.get('name').upper()} REACHED LEVEL {res['new_level']}!", width=70, color=BRIGHT_YELLOW))
    print(f"  {BOLD}Hit Points Gained:{RESET} {GREEN}+{res['hp_gain']} HP{RESET} (New Max: {BOLD}{res['new_max_hp']}{RESET})")
    print(f"  {BOLD}Proficiency Bonus:{RESET} +{char.get('proficiency_bonus')}")
    if res.get("new_features"):
        print(f"  {BOLD}New Features Unlocked:{RESET}")
        for feat in res["new_features"]:
            print(f"   • {feat}")
    print()
    print(inspector.render_character_sheet(char))


def cmd_inspect(args):
    """Displays full character sheet, inventory, spell slots, and traits."""
    inspector = CharacterInspector(str(PROJECT_ROOT))
    mp = MultiplayerManager(str(PROJECT_ROOT))
    
    char_target = args.character
    if not char_target:
        active = mp.get_active_player()
        char_target = active.get("id") if active else None

    if not char_target:
        print("Error: No character specified or found in party.", file=sys.stderr)
        sys.exit(1)

    res = inspector.inspect_character(char_target)
    if not res["success"]:
        print(f"Error: {res['error']}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(res["character"], indent=2))
        return

    tab = getattr(args, "tab", "all")
    print(inspector.render_character_sheet(res["character"], tab=tab))


def cmd_party(args):
    """Manages the party roster and active player selection."""
    mp = MultiplayerManager(str(PROJECT_ROOT))
    party = mp.get_party()
    active_player = mp.get_active_player()
    active_id = active_player.get("id") if active_player else None

    if args.action == "list":
        if args.json:
            print(json.dumps({"active_id": active_id, "party": party}, indent=2))
            return
        print("\n" + box_header("PARTY ROSTER & MULTI-PLAYER ROLES", width=70, color=BRIGHT_CYAN))
        for p in party:
            is_active = p.get("id") == active_id
            act_badge = f" {badge('ACTIVE PLAYER', 'active')}" if is_active else ""
            ctrl = "Human Player" if p.get("is_player", True) else "AI Companion"
            hp = p.get("hp", {})
            hp_bar = render_hp_bar(hp.get("current", 10), hp.get("max", 10), hp.get("temp", 0))
            print(f"* [{BOLD}{p.get('id')}{RESET}] {BOLD}{p.get('name')}{RESET} (Lvl {p.get('level', 1)} {p.get('class', '')} [{ctrl}]){act_badge}")
            print(f"  Health: {hp_bar} | AC: {BOLD}{p.get('ac')}{RESET}")
        print()
    elif args.action == "switch" or args.action == "activate":
        if not args.character_id:
            print("Error: Specify character ID to switch to.", file=sys.stderr)
            sys.exit(1)
        res = mp.set_active_player(args.character_id)
        if not res["success"]:
            print(f"Error: {res['error']}", file=sys.stderr)
            sys.exit(1)
        if args.json:
            print(json.dumps(res, indent=2))
            return
        print(f"\n{GREEN}▶ Switched active player to:{RESET} {BOLD}{res['active_character'].get('name')}{RESET} ({res['active_character'].get('class')})\n")


def cmd_initiative(args):
    """Manages combat initiative turn order."""
    mp = MultiplayerManager(str(PROJECT_ROOT))
    sm, _, _, _ = get_managers()

    if args.action == "roll":
        monsters = []
        if getattr(args, "monsters", None):
            for m_name in args.monsters.split(","):
                m_name = m_name.strip()
                if not m_name:
                    continue
                m_stat = sm.get_npc(m_name)
                if m_stat:
                    monsters.append(m_stat)
                else:
                    monsters.append({"name": m_name, "stats": {"dexterity": 12}, "ac": 13, "hp": {"current": 15, "max": 15}})

        combat = mp.roll_initiative(monsters=monsters, seed=args.seed)
        if args.json:
            print(json.dumps(combat, indent=2))
            return
        print("\n" + box_header(f"INITIATIVE ROLLED — COMBAT ROUND {combat['round']}", width=70, color=BRIGHT_RED))
        for i, c in enumerate(combat["order"]):
            cur_marker = f" {badge('CURRENT TURN', 'crit')}" if i == combat["turn_index"] else ""
            type_str = "Monster" if c.get("is_monster") else ("Player" if c.get("is_player") else "Companion")
            print(f"  [{c['initiative']:2d}] {BOLD}{c['name']}{RESET} ({type_str}){cur_marker}")
        print()
    elif args.action == "show":
        combat = mp.get_initiative()
        if not combat.get("in_combat") or not combat.get("order"):
            print("\nNo combat currently active. Run 'python dnd.py initiative roll' to start.\n")
            return
        if args.json:
            print(json.dumps(combat, indent=2))
            return
        print("\n" + box_header(f"INITIATIVE ORDER — ROUND {combat.get('round', 1)}", width=70, color=BRIGHT_YELLOW))
        for i, c in enumerate(combat.get("order", [])):
            is_turn = i == combat.get("turn_index", 0)
            cur_marker = f" {badge('ACTIVE TURN', 'crit')}" if is_turn else ""
            print(f"  [{c['initiative']:2d}] {BOLD}{c['name']}{RESET}{cur_marker}")
        print()
    elif args.action == "next":
        res = mp.advance_turn()
        if not res["success"]:
            print(f"Error: {res['error']}", file=sys.stderr)
            sys.exit(1)
        if args.json:
            print(json.dumps(res, indent=2))
            return
        cur = res["current_combatant"]
        print(f"\n{BRIGHT_GREEN}▶ ADVANCED TURN TO ROUND {res['round']}:{RESET} {BOLD}{cur.get('name')}{RESET} (Init: {cur.get('initiative')})\n")
    elif args.action == "end":
        res = mp.end_combat()
        print(f"\n{GREEN}{res['message']}{RESET}\n")


def cmd_dev(args):
    """Executes a Developer Agent task in Developer Mode."""
    _, _, _, dev = get_managers()
    prompt = " ".join(args.prompt)
    res = dev.execute_developer_task(prompt)
    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"Developer Agent Task: {prompt}")
        print(json.dumps(res, indent=2))


def cmd_menu(args):
    """Displays the comprehensive game dashboard, active hero HUD, and action menu."""
    from tools.menu import render_game_menu, get_boot_context
    if getattr(args, "json", False):
        print(json.dumps(get_boot_context(str(PROJECT_ROOT)), indent=2))
    else:
        print("\n" + render_game_menu(project_root=str(PROJECT_ROOT)))


def cmd_boot(args):
    """Executes fast-boot session initialization and returns full state summary."""
    from tools.menu import get_boot_context, render_game_menu
    ctx = get_boot_context(str(PROJECT_ROOT))
    if getattr(args, "json", False):
        print(json.dumps(ctx, indent=2))
    else:
        print("\n" + render_game_menu(context=ctx, project_root=str(PROJECT_ROOT)))


def cmd_loot(args):
    """Generates individual or hoard treasure based on Challenge Rating (CR)."""
    from tools.loot import LootGenerator
    lg = LootGenerator(str(PROJECT_ROOT))
    if getattr(args, "hoard", False):
        res = lg.generate_hoard_treasure(cr=args.cr, seed=args.seed)
    else:
        res = lg.generate_individual_treasure(cr=args.cr, seed=args.seed)
    
    if getattr(args, "json", False):
        print(json.dumps(res, indent=2))
    else:
        print(f"\n=== 💰 5e Treasure Drop (CR {res['cr']} {'Hoard' if res['type']=='hoard_treasure' else 'Individual'}) ===")
        coins_str = ", ".join(f"{v} {k.upper()}" for k, v in res.get("coins", {}).items() if v > 0)
        print(f"Coins: {coins_str or 'None'}")
        if res.get("gems_and_art"):
            print("Gems & Art Objects:")
            for ga in res["gems_and_art"]:
                print(f" • {ga['description']} (Total: {ga['total_gp']} gp)")
        if res.get("magic_items"):
            print("Magic Items:")
            for item in res["magic_items"]:
                source_badge = f" [{item.get('source')}]" if item.get("source") else ""
                print(f" • {item['name']} ({item['rarity']} {item['type']}){source_badge}")
        print(f"Total Value: ~{res['total_value_gp']} gp\n")


def cmd_explain(args):
    """Explains a D&D 2024 rule, weapon mastery, condition, or spellcasting mechanic."""
    from tools.explainer import explain_mechanic
    res = explain_mechanic(args.topic)
    if getattr(args, "json", False):
        print(json.dumps(res, indent=2))
        return
    if not res.get("found"):
        print(f"\n{RED}✗ {res.get('error')}{RESET}")
        if res.get("suggestions"):
            print(f"  Did you mean: {', '.join(res['suggestions'])}\n")
        return
    print(f"\n" + "=" * 65)
    print(f"📖 D&D 2024 MECHANICS EXPLAINER: {res['topic'].upper()}")
    print(f"Category: [{res['category']}] | Source: {res['rule_source']}")
    print("=" * 65)
    print(res["explanation"])
    print("=" * 65 + "\n")


def cmd_compendium(args):
    """Validates rules compendiums or displays entity statistics."""
    from tools.compendium_validator import CompendiumValidator
    cv = CompendiumValidator(str(PROJECT_ROOT))
    if args.action == "validate":
        res = cv.validate_all()
        if getattr(args, "json", False):
            print(json.dumps(res, indent=2))
        else:
            if res["valid"]:
                print(f"\n{GREEN}✓ COMPENDIUM VALIDATION PASSED:{RESET} {res['total_entities']} entities validated across all rules schemas with 0 errors.\n")
            else:
                print(f"\n{RED}✗ COMPENDIUM VALIDATION FAILED:{RESET} Found {len(res['errors'])} errors:")
                for err in res["errors"]:
                    print(f" • {err}")
                print()
    elif args.action == "stats":
        stats = cv.get_stats()
        if getattr(args, "json", False):
            print(json.dumps(stats, indent=2))
        else:
            print(f"\n=== 📚 D&D 5e Rules Compendium Statistics ===")
            for cat, count in stats["entity_counts"].items():
                print(f" • {cat.replace('_', ' ').title():<18}: {count} entries")
            print(f"Total Registered Entities: {stats['total_entities']}\n")


def main():
    # If no arguments provided, default to displaying the interactive menu dashboard
    if len(sys.argv) == 1:
        from tools.menu import render_game_menu
        print("\n" + render_game_menu(project_root=str(PROJECT_ROOT)))
        return

    parser = argparse.ArgumentParser(description="Agentic D&D CLI Router & Game Engine")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # menu / dashboard
    p_menu = subparsers.add_parser("menu", help="Display interactive game dashboard and non-developer action menu")
    p_menu.add_argument("--json", action="store_true", help="Output JSON context")
    p_menu.set_defaults(func=cmd_menu)

    # boot
    p_boot = subparsers.add_parser("boot", help="Fast-boot session initialization and state snapshot")
    p_boot.add_argument("--json", action="store_true", help="Output JSON context")
    p_boot.set_defaults(func=cmd_boot)

    # play
    p_play = subparsers.add_parser("play", help="Execute natural language player intent")
    p_play.add_argument("intent", nargs="+", help="Natural language action")
    p_play.add_argument("--character", "-c", default=None, help="Character ID")
    p_play.add_argument("--seed", "-s", type=int, default=None, help="RNG seed")
    p_play.add_argument("--no-commit", action="store_true", help="Do not commit snapshot")
    p_play.add_argument("--json", action="store_true", help="Output raw JSON trace")
    p_play.set_defaults(func=cmd_play)

    # status
    p_status = subparsers.add_parser("status", help="Display party & scene status")
    p_status.add_argument("--json", action="store_true", help="Output full JSON state")
    p_status.set_defaults(func=cmd_status)

    # roll
    p_roll = subparsers.add_parser("roll", help="Roll tabletop dice deterministically")
    p_roll.add_argument("expression", nargs="?", default="1d20", help="Dice expression (e.g. 1d20+5, 2d6+3)")
    p_roll.add_argument("--adv", action="store_true", help="Roll with Advantage")
    p_roll.add_argument("--disadv", action="store_true", help="Roll with Disadvantage")
    p_roll.add_argument("--crit", action="store_true", help="Double dice count (Critical Hit)")
    p_roll.add_argument("--bonus", "-b", type=int, default=0, help="Additional bonus")
    p_roll.add_argument("--seed", "-s", type=int, default=None, help="RNG seed")
    p_roll.add_argument("--json", action="store_true", help="Output JSON")
    p_roll.set_defaults(func=cmd_roll)

    # check
    p_check = subparsers.add_parser("check", help="Roll D&D 2024 ability or skill check")
    p_check.add_argument("skill", help="Skill or ability name (e.g. stealth, perception, athletics)")
    p_check.add_argument("dc", nargs="?", type=int, default=15, help="Difficulty Class (default: 15)")
    p_check.add_argument("--character", "-c", default=None, help="Character ID")
    p_check.add_argument("--adv", action="store_true", help="Advantage")
    p_check.add_argument("--disadv", action="store_true", help="Disadvantage")
    p_check.add_argument("--guidance", action="store_true", help="Add 1d4 Guidance")
    p_check.add_argument("--bonus", "-b", type=int, default=0, help="Extra bonus")
    p_check.add_argument("--seed", "-s", type=int, default=None, help="RNG seed")
    p_check.add_argument("--json", action="store_true", help="Output JSON")
    p_check.set_defaults(func=cmd_check)

    # rest
    p_rest = subparsers.add_parser("rest", help="Take a short or long rest")
    p_rest.add_argument("type", choices=["short", "long"], default="short", nargs="?", help="Rest type (short or long)")
    p_rest.add_argument("--character", "-c", default=None, help="Specific character ID")
    p_rest.add_argument("--hit-dice", "-d", type=int, default=1, help="Hit Dice to spend during short rest")
    p_rest.add_argument("--seed", "-s", type=int, default=None, help="RNG seed")
    p_rest.add_argument("--json", action="store_true", help="Output JSON")
    p_rest.set_defaults(func=cmd_rest)

    # cast
    p_cast = subparsers.add_parser("cast", help="Cast a spell from the PHB compendium")
    p_cast.add_argument("spell", help="Spell name (e.g. fire_bolt, cure_wounds, magic_missile)")
    p_cast.add_argument("--character", "-c", default=None, help="Caster Character ID")
    p_cast.add_argument("--target", "-t", default=None, help="Target Character or NPC ID")
    p_cast.add_argument("--level", "-l", type=int, default=None, help="Upcast spell slot level")
    p_cast.add_argument("--ritual", "-r", action="store_true", help="Cast as a ritual (10 min, 0 slots)")
    p_cast.add_argument("--seed", "-s", type=int, default=None, help="RNG seed")
    p_cast.add_argument("--json", action="store_true", help="Output JSON")
    p_cast.set_defaults(func=cmd_cast)

    # spell
    p_spell = subparsers.add_parser("spell", help="Display spell details from PHB")
    p_spell.add_argument("name", help="Spell name or ID (e.g. fireball, misty_step)")
    p_spell.add_argument("--json", action="store_true", help="Output JSON")
    p_spell.set_defaults(func=cmd_spell)

    # death-save
    p_ds = subparsers.add_parser("death-save", help="Roll death saving throw at 0 HP")
    p_ds.add_argument("--character", "-c", default=None, help="Character ID")
    p_ds.add_argument("--seed", "-s", type=int, default=None, help="RNG seed")
    p_ds.add_argument("--json", action="store_true", help="Output JSON")
    p_ds.set_defaults(func=cmd_death_save)

    # stabilize
    p_stab = subparsers.add_parser("stabilize", help="Stabilize an unconscious ally (DC 10 Medicine)")
    p_stab.add_argument("target", help="Unconscious Character ID")
    p_stab.add_argument("--healer", "-a", default=None, help="Healer Character ID")
    p_stab.add_argument("--seed", "-s", type=int, default=None, help="RNG seed")
    p_stab.add_argument("--json", action="store_true", help="Output JSON")
    p_stab.set_defaults(func=cmd_stabilize)

    # attack
    p_atk = subparsers.add_parser("attack", help="Execute attack and damage rolls")
    p_atk.add_argument("target", help="Target name or NPC ID")
    p_atk.add_argument("--attacker", "-a", default=None, help="Attacker Character ID")
    p_atk.add_argument("--weapon", "-w", default=None, help="Weapon name")
    p_atk.add_argument("--ac", type=int, default=None, help="Override target AC")
    p_atk.add_argument("--cover", choices=["none", "half", "three_quarters", "total"], default="none", help="Cover type")
    p_atk.add_argument("--adv", action="store_true", help="Advantage")
    p_atk.add_argument("--disadv", action="store_true", help="Disadvantage")
    p_atk.add_argument("--bonus", "-b", type=int, default=0, help="Attack bonus")
    p_atk.add_argument("--seed", "-s", type=int, default=None, help="RNG seed")
    p_atk.add_argument("--json", action="store_true", help="Output JSON")
    p_atk.set_defaults(func=cmd_attack)

    # encounter
    p_enc = subparsers.add_parser("encounter", help="Calculate encounter difficulty and XP budget")
    p_enc.add_argument("--preset", default=None, help="Curated adventure encounter preset ID (e.g. 'goblin_ambush', 'klargs_den')")
    p_enc.add_argument("--monsters", "-m", default=None, help="Monsters list (e.g. 'bugbear:1,hobgoblin:3' or 'cr1:2')")
    p_enc.add_argument("--party", "-p", default=None, help="Comma-separated party levels (e.g. '3,3,3,2')")
    p_enc.add_argument("--situational", "-s", type=int, default=0, help="-1 for party benefit, +1 for drawback")
    p_enc.add_argument("--json", action="store_true", help="Output JSON")
    p_enc.set_defaults(func=cmd_encounter)

    # monster
    p_mon = subparsers.add_parser("monster", help="Display monster statblock from Basic Rules")
    p_mon.add_argument("name", help="Monster name or ID (e.g. goblin, guard, adult_red_dragon)")
    p_mon.add_argument("--json", action="store_true", help="Output JSON")
    p_mon.set_defaults(func=cmd_monster)

    # item
    p_item = subparsers.add_parser("item", help="Display magic item from Basic Rules")
    p_item.add_argument("name", help="Magic item name or ID (e.g. bag_of_holding, cloak_of_elvenkind)")
    p_item.add_argument("--json", action="store_true", help="Output JSON")
    p_item.set_defaults(func=cmd_item)

    # history
    p_hist = subparsers.add_parser("history", help="Show Git-style commit timeline")
    p_hist.add_argument("--branch", default=None, help="Target branch")
    p_hist.add_argument("--limit", type=int, default=10, help="Number of commits to show")
    p_hist.add_argument("--json", action="store_true", help="Output JSON")
    p_hist.set_defaults(func=cmd_history)

    # diff
    p_diff = subparsers.add_parser("diff", help="Show unified state diff")
    p_diff.add_argument("commit_b", help="Newer commit ID")
    p_diff.add_argument("commit_a", nargs="?", default=None, help="Older commit ID (optional)")
    p_diff.add_argument("--json", action="store_true", help="Output JSON")
    p_diff.set_defaults(func=cmd_diff)

    # rollback
    p_rb = subparsers.add_parser("rollback", help="Restore campaign to a snapshot commit")
    p_rb.add_argument("commit_id", help="Commit ID to restore")
    p_rb.set_defaults(func=cmd_rollback)

    # branch
    p_br = subparsers.add_parser("branch", help="Create or switch branch timeline")
    p_br.add_argument("branch_name", help="Branch name")
    p_br.add_argument("--create", "-c", action="store_true", help="Create new branch")
    p_br.set_defaults(func=cmd_branch)

    # test
    p_test = subparsers.add_parser("test", help="Run automated test suite")
    p_test.add_argument("--pattern", default="test_*.py", help="Test file pattern")
    p_test.set_defaults(func=cmd_test)

    # explain
    p_exp = subparsers.add_parser("explain", help="Explain a D&D 2024 rule, weapon mastery, condition, or mechanic")
    p_exp.add_argument("topic", help="Topic name (e.g. 'topple', 'vex', 'death_saves', 'cover', 'blinded', 'ritual')")
    p_exp.add_argument("--json", action="store_true", help="Output JSON")
    p_exp.set_defaults(func=cmd_explain)

    # create-character
    p_cc = subparsers.add_parser("create-character", help="Create a new D&D 5e character")
    p_cc.add_argument("--name", "-n", default=None, help="Character name (optional if using --preset or --interactive)")
    p_cc.add_argument("--class", "-c", dest="char_class", default="Fighter", help="Class (Fighter, Wizard, Rogue, Cleric, Paladin, Barbarian, Ranger, Druid, Monk, Bard, Sorcerer, Warlock)")
    p_cc.add_argument("--species", "-s", default="Human", help="Species/Subrace (Human, Variant Human, High Elf, Wood Elf, Drow, Hill Dwarf, Mountain Dwarf, Lightfoot Halfling, Stout Halfling, Dragonborn, Forest Gnome, Rock Gnome, Half-Elf, Half-Orc, Tiefling)")
    p_cc.add_argument("--background", "-b", default="Soldier", help="Background (Soldier, Criminal, Sage, Acolyte, Folk Hero, Noble, Outlander, Urchin)")
    p_cc.add_argument("--method", "-m", choices=["standard", "roll"], default="standard", help="Ability score method")
    p_cc.add_argument("--scores", help="Custom scores: 'STR,DEX,CON,INT,WIS,CHA' (e.g. '16,14,14,10,12,8')")
    p_cc.add_argument("--preset", "-p", choices=list(LMOP_PRESETS.keys()), help="Load iconic LMoP Starter Set pre-generated character archetype")
    p_cc.add_argument("--interactive", "-i", action="store_true", help="Launch interactive step-by-step terminal wizard")
    p_cc.add_argument("--companion", action="store_true", help="Set as AI companion instead of player character")
    p_cc.add_argument("--activate", action="store_true", help="Set as active player character immediately")
    p_cc.add_argument("--seed", type=int, default=None, help="RNG seed for score rolls")
    p_cc.add_argument("--json", action="store_true", help="Output JSON")
    p_cc.set_defaults(func=cmd_create_character)

    # level-up
    p_lvl = subparsers.add_parser("level-up", help="Level up a character to the next level (1-20)")
    p_lvl.add_argument("character", nargs="?", default=None, help="Character ID or name (defaults to active player)")
    p_lvl.add_argument("--roll", "-r", action="store_true", help="Roll Hit Die for HP instead of average")
    p_lvl.add_argument("--seed", "-s", type=int, default=None, help="RNG seed for HP roll")
    p_lvl.add_argument("--json", action="store_true", help="Output JSON")
    p_lvl.set_defaults(func=cmd_level_up)

    # inspect & character alias
    p_insp = subparsers.add_parser("inspect", help="Inspect character profile, inventory, skills & spells")
    p_insp.add_argument("character", nargs="?", default=None, help="Character ID or name (defaults to active player)")
    p_insp.add_argument("--tab", choices=["all", "bio", "stats", "attacks", "spells", "inventory"], default="all", help="Specific view tab")
    p_insp.add_argument("--json", action="store_true", help="Output JSON")
    p_insp.set_defaults(func=cmd_inspect)

    p_char = subparsers.add_parser("character", help="Inspect character sheet (alias for inspect)")
    p_char.add_argument("character", nargs="?", default=None, help="Character ID or name")
    p_char.add_argument("--tab", default="all", help="View tab")
    p_char.add_argument("--json", action="store_true", help="Output JSON")
    p_char.set_defaults(func=cmd_inspect)

    # party
    p_pty = subparsers.add_parser("party", help="Manage multiplayer party and active player")
    p_pty.add_argument("action", choices=["list", "switch", "activate"], default="list", nargs="?", help="Party action")
    p_pty.add_argument("character_id", nargs="?", default=None, help="Character ID to switch to")
    p_pty.add_argument("--json", action="store_true", help="Output JSON")
    p_pty.set_defaults(func=cmd_party)

    # initiative
    p_init = subparsers.add_parser("initiative", help="Manage combat initiative turn order")
    p_init.add_argument("action", choices=["roll", "show", "next", "end"], default="show", nargs="?", help="Initiative action")
    p_init.add_argument("--monsters", "-m", default=None, help="Comma-separated monster names/IDs")
    p_init.add_argument("--seed", "-s", type=int, default=None, help="RNG seed")
    p_init.add_argument("--json", action="store_true", help="Output JSON")
    p_init.set_defaults(func=cmd_initiative)

    # adventure
    p_adv = subparsers.add_parser("adventure", help="Manage modular adventure packages (list, info, load, new)")
    p_adv.add_argument("action", choices=["list", "info", "load", "new", "scaffold"], help="Adventure action")
    p_adv.add_argument("adventure_id", nargs="?", default=None, help="Adventure slug (e.g. 'lost_mine_of_phandelver')")
    p_adv.add_argument("--title", default=None, help="Adventure title (for 'new')")
    p_adv.add_argument("--levels", default="1-5", help="Recommended levels (for 'new')")
    p_adv.add_argument("--json", action="store_true", help="Output JSON")
    p_adv.set_defaults(func=cmd_adventure)

    # dev
    p_dev = subparsers.add_parser("dev", help="Execute developer task in Developer Mode")
    p_dev.add_argument("prompt", nargs="+", help="Developer instructions")
    p_dev.add_argument("--json", action="store_true", help="Output JSON")
    p_dev.set_defaults(func=cmd_dev)

    # loot
    p_loot = subparsers.add_parser("loot", help="Generate individual or hoard treasure by Challenge Rating (CR)")
    p_loot.add_argument("--cr", type=float, default=1.0, help="Monster or Encounter Challenge Rating (default: 1.0)")
    p_loot.add_argument("--hoard", action="store_true", help="Generate a full dungeon treasure hoard")
    p_loot.add_argument("--seed", "-s", type=int, default=None, help="RNG seed")
    p_loot.add_argument("--json", action="store_true", help="Output JSON")
    p_loot.set_defaults(func=cmd_loot)

    # compendium
    p_comp = subparsers.add_parser("compendium", help="Validate rules compendiums or display catalog statistics")
    p_comp.add_argument("action", choices=["validate", "stats"], default="validate", nargs="?", help="Compendium action")
    p_comp.add_argument("--json", action="store_true", help="Output JSON")
    p_comp.set_defaults(func=cmd_compendium)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
