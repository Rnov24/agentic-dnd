"""
Fast-Boot Dashboard & Non-Developer Action Menu Engine for Agentic D&D.
Provides instant session boot context, active character HUD, and a comprehensive,
user-friendly action menu for tabletop players.
"""

import json
from typing import Dict, Any, Optional, List
from pathlib import Path
from tools.state_manager import StateManager
from tools.multiplayer import MultiplayerManager
from tools.formatting import (
    render_hp_bar, render_slot_pips, box_header, box_section,
    badge, BOLD, RESET, DIM, CYAN, GREEN, YELLOW, MAGENTA, RED,
    BRIGHT_YELLOW, BRIGHT_CYAN, BRIGHT_GREEN, BRIGHT_RED, BRIGHT_MAGENTA
)


_BOOT_CACHE: Optional[Dict[str, Any]] = None
_CACHE_TIMESTAMP: float = 0.0


def get_boot_context(project_root: Optional[str] = None, force_refresh: bool = False) -> Dict[str, Any]:
    """
    Rapidly loads and returns an all-in-one game context snapshot.
    Uses transparent in-memory short-lived caching for sub-millisecond warm calls.
    """
    global _BOOT_CACHE, _CACHE_TIMESTAMP
    import time
    now = time.time()
    if _BOOT_CACHE is not None and not force_refresh and (now - _CACHE_TIMESTAMP < 1.0):
        return _BOOT_CACHE

    sm = StateManager(project_root)
    mp = MultiplayerManager(project_root)
    
    world = sm.get_world()
    party = sm.get_party()
    npcs = sm.get_npcs()
    quests = sm.get_quests()
    combat = sm.get_combat()
    active_player = mp.get_active_player() or (party[0] if party else {})
    
    context = {
        "campaign_name": world.get("campaign_name", "Agentic D&D"),
        "location": world.get("active_location", "Unknown"),
        "time_of_day": world.get("time_of_day", "Day"),
        "weather": world.get("weather", "Clear"),
        "lighting": world.get("lighting", "Bright Light"),
        "tension": world.get("tension_level", "Calm"),
        "in_combat": combat.get("in_combat", False),
        "scene": world.get("current_scene", {}),
        "active_player": active_player,
        "party_roster": party,
        "npcs": npcs,
        "quests": quests,
        "combat": combat
    }
    
    _BOOT_CACHE = context
    _CACHE_TIMESTAMP = now
    return context


def render_game_menu(
    context: Optional[Dict[str, Any]] = None,
    project_root: Optional[str] = None,
    width: int = 70
) -> str:
    """
    Renders a comprehensive, non-developer visual dashboard and interactive action menu.
    """
    if context is None:
        context = get_boot_context(project_root)

    camp_name = context.get("campaign_name", "Agentic D&D")
    loc = context.get("location", "Wilderness")
    time_of_day = context.get("time_of_day", "Late Afternoon")
    weather = context.get("weather", "Overcast")
    lighting = context.get("lighting", "Dim")
    tension = context.get("tension", "Tense")
    in_combat = context.get("in_combat", False)
    
    active = context.get("active_player", {})
    scene = context.get("scene", {})
    party = context.get("party_roster", [])
    
    lines = []
    
    # 1. Main Header
    header_title = f"⚔️  {camp_name.upper()} — GAME DASHBOARD  ⚔️"
    lines.append(box_header(header_title, width=width, color=BRIGHT_CYAN))
    lines.append(f"  {BOLD}Location:{RESET} {loc} | {BOLD}Time:{RESET} {time_of_day} | {BOLD}Weather:{RESET} {weather}")
    lines.append(f"  {BOLD}Lighting:{RESET} {lighting} | {BOLD}Tension:{RESET} {tension} | {BOLD}State:{RESET} {'⚔️ IN COMBAT' if in_combat else '🌲 Exploration'}")

    # 2. Scene Snapshot (Theater of the Mind)
    if scene and scene.get("title"):
        lines.append(box_section(f"CURRENT SCENE: {scene.get('title')}", color=CYAN))
        desc = scene.get("description", "")
        if desc:
            lines.append(f"  {desc}")
        if scene.get("threats"):
            lines.append(f"\n  {BRIGHT_RED}⚠️ Active Threats:{RESET}")
            for t in scene["threats"]:
                lines.append(f"   • {t}")
        if scene.get("exits"):
            lines.append(f"\n  {GREEN}🚪 Exits & Paths:{RESET}")
            for e in scene["exits"]:
                lines.append(f"   • {e}")

    # 3. Active Player HUD
    if active:
        p_name = active.get("name", "Unknown Hero")
        p_lvl = active.get("level", 1)
        p_cls = active.get("class", "Adventurer")
        p_species = active.get("species", active.get("race", "Human"))
        p_ac = active.get("ac", 10)
        p_hp = active.get("hp", {})
        cur_hp = p_hp.get("current", 10) if p_hp.get("current") is not None else p_hp.get("max", 10)
        max_hp = p_hp.get("max", 10)
        tmp_hp = p_hp.get("temp", 0) or 0
        hd = active.get("hit_dice", {})
        hd_str = f"{hd.get('current', 1)}/{hd.get('max', 1)} ({hd.get('die', '1d8')})" if isinstance(hd, dict) else str(hd)
        conds = ", ".join(active.get("conditions", [])) if active.get("conditions") else "None"
        
        lines.append(box_section(f"ACTIVE HERO: {p_name} (Lvl {p_lvl} {p_species} {p_cls})", color=BRIGHT_YELLOW))
        lines.append(f"  Health:    {render_hp_bar(cur_hp, max_hp, tmp_hp)}")
        lines.append(f"  Armor Class: {BOLD}{p_ac}{RESET} | Hit Dice: {BOLD}{hd_str}{RESET} | Conditions: {conds}")
        
        # Spell slots if caster
        if "spell_slots" in active and active["spell_slots"]:
            slot_strs = [f"Lvl {k.split('_')[1]}: {render_slot_pips(v.get('current', 0), v.get('max', 0))}" for k, v in active["spell_slots"].items()]
            lines.append(f"  Spell Slots: {' | '.join(slot_strs)}")
        if active.get("cantrips"):
            lines.append(f"  Cantrips:   {', '.join(active.get('cantrips', []))}")
        if active.get("languages"):
            lines.append(f"  Languages:  {', '.join(active.get('languages', []))}")

    # 4. Party Roster Strip
    if len(party) > 1:
        lines.append(box_section("PARTY ROSTER", color=YELLOW))
        roster_items = []
        for p in party:
            is_active = p.get("id") == active.get("id")
            marker = f"{BRIGHT_GREEN}▶{RESET} " if is_active else "  "
            p_hp_val = p.get("hp", {})
            hp_cur = p_hp_val.get("current", 10) if p_hp_val.get("current") is not None else p_hp_val.get("max", 10)
            hp_max = p_hp_val.get("max", 10)
            roster_items.append(f"{marker}{BOLD}{p.get('name')}{RESET} ({p.get('class', '')} {hp_cur}/{hp_max} HP)")
        lines.append(" | ".join(roster_items[:3]))
        if len(roster_items) > 3:
            lines.append(" | ".join(roster_items[3:6]))
        if len(roster_items) > 6:
            lines.append(" | ".join(roster_items[6:]))

    # 5. Non-Developer Action Menu & Quick Commands
    lines.append(box_section("🎮 WHAT WOULD YOU LIKE TO DO? (ACTION MENU)", color=BRIGHT_GREEN))
    
    lines.append(f"  {BOLD}💬 Natural Language (Just type what you want to do):{RESET}")
    lines.append(f"    • {CYAN}\"I attack the goblin in front of me with my sword\"{RESET}")
    lines.append(f"    • {CYAN}\"I cast Fire Bolt at the nearest goblin archer\"{RESET}")
    lines.append(f"    • {CYAN}\"I quietly search the bushes for tracks or hidden enemies\"{RESET}")
    lines.append(f"    • {CYAN}\"We take a short rest and bandage our wounds\"{RESET}")
    lines.append(f"    • {CYAN}\"I talk to Sildar and ask what happened on the road\"{RESET}")
    
    lines.append(f"\n  {BOLD}⚡ Quick Slash Commands & Tool Shortcuts:{RESET}")
    lines.append(f"  {BRIGHT_YELLOW}[1] Play Action{RESET}   : {BOLD}python dnd.py play \"<intent>\"{RESET} (Full turn orchestration)")
    lines.append(f"  {BRIGHT_YELLOW}[2] Attack Target{RESET} : {BOLD}python dnd.py attack <target> [--cover half]{RESET}")
    lines.append(f"  {BRIGHT_YELLOW}[3] Cast Spell{RESET}    : {BOLD}python dnd.py cast <spell> [--target <target>]{RESET}")
    lines.append(f"  {BRIGHT_YELLOW}[4] Skill Check{RESET}   : {BOLD}python dnd.py check <stealth/perception/athletics> [dc]{RESET}")
    lines.append(f"  {BRIGHT_YELLOW}[5] Roll Tabletop{RESET} : {BOLD}python dnd.py roll \"1d20+5 --adv\"{RESET} / {BOLD}\"2d6+3\"{RESET}")
    lines.append(f"  {BRIGHT_YELLOW}[6] Inspect Sheet{RESET} : {BOLD}python dnd.py inspect [character_name]{RESET}")
    lines.append(f"  {BRIGHT_YELLOW}[7] Switch Player{RESET} : {BOLD}python dnd.py party switch <character_name>{RESET}")
    lines.append(f"  {BRIGHT_YELLOW}[8] Short/Long Rest{RESET}: {BOLD}python dnd.py rest short{RESET} / {BOLD}python dnd.py rest long{RESET}")
    lines.append(f"  {BRIGHT_YELLOW}[9] Lookup Rules{RESET}  : {BOLD}python dnd.py spell <name>{RESET} / {BOLD}monster <name>{RESET} / {BOLD}item <name>{RESET}")
    lines.append(f"  {BRIGHT_YELLOW}[10] Status/Quests{RESET}: {BOLD}python dnd.py status{RESET} / {BOLD}python dnd.py menu{RESET}")

    lines.append("\n" + "=" * width + "\n")
    return "\n".join(lines)

