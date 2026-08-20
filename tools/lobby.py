"""
Campaign Launcher & Pre-Run Setup Lobby for Agentic D&D.
Renders the interactive setup lobby where players select/create campaign runs,
configure difficulty modes, and assemble their party roster before entering the field.
"""

from typing import Dict, Any, Optional
from pathlib import Path
from tools.run_manager import RunManager, DIFFICULTY_PRESETS
from tools.vault import CharacterVault
from tools.formatting import (
    box_header, box_section, render_hp_bar,
    BOLD, RESET, DIM, CYAN, GREEN, YELLOW, MAGENTA, RED,
    BRIGHT_YELLOW, BRIGHT_CYAN, BRIGHT_GREEN, BRIGHT_RED, BRIGHT_MAGENTA
)


def render_campaign_lobby(project_root: Optional[str] = None, width: int = 70) -> str:
    """
    Renders the Campaign Setup & Pre-Run Launcher Lobby.
    """
    rm = RunManager(project_root)
    vault = CharacterVault(project_root)
    
    runs = rm.list_runs()
    active_manifest = rm.get_active_run_manifest()
    vault_chars = vault.list_characters()
    
    lines = []
    
    # 1. Lobby Header
    lines.append(box_header("🏰 AGENTIC D&D — CAMPAIGN LAUNCHER & RUN SETUP 🏰", width=width, color=BRIGHT_MAGENTA))
    lines.append(f"  {DIM}Configure your campaign run, select difficulty, and assemble your party roster.{RESET}")

    # 2. Active Run Info
    if active_manifest:
        run_name = active_manifest.get("name", "Active Run")
        run_id = active_manifest.get("id")
        adv = active_manifest.get("adventure", "Custom")
        diff_id = active_manifest.get("difficulty", "normal")
        diff_info = DIFFICULTY_PRESETS.get(diff_id, DIFFICULTY_PRESETS["normal"])
        turns = active_manifest.get("turns_count", 0)
        
        lines.append(box_section(f"ACTIVE CAMPAIGN RUN: [{run_name}]", color=BRIGHT_GREEN))
        lines.append(f"  {BOLD}Run ID:{RESET} {CYAN}{run_id}{RESET} | {BOLD}Adventure:{RESET} {adv} | {BOLD}Turns Played:{RESET} {turns}")
        lines.append(f"  {BOLD}Difficulty:{RESET} {diff_info['badge']} — {DIM}{diff_info['description']}{RESET}")
    else:
        lines.append(box_section("ACTIVE CAMPAIGN RUN", color=YELLOW))
        lines.append(f"  {YELLOW}No active run selected.{RESET} Running on standard workspace state.")
        lines.append(f"  Create a new run below or switch to an existing save slot.")

    # 3. Available Campaign Runs / Save Slots
    lines.append(box_section("📂 CAMPAIGN RUNS & SAVE SLOTS", color=CYAN))
    if runs:
        for r in runs:
            marker = f"{BRIGHT_GREEN}▶ [ACTIVE]{RESET}" if r.get("is_active") else "  [SLOT]  "
            diff_badge = DIFFICULTY_PRESETS.get(r.get("difficulty", "normal"), {}).get("badge", r.get("difficulty"))
            p_count = len(r.get("party_ids", []))
            lines.append(f"  {marker} {BOLD}{r.get('name')}{RESET} (ID: `{r.get('id')}`) | {diff_badge} | {p_count} Heroes")
    else:
        lines.append(f"  {DIM}No saved runs created yet. (Run 'python dnd.py run new' to create one){RESET}")

    # 4. Difficulty Modes Reference
    lines.append(box_section("⚙️ DIFFICULTY MODES & RULES MODIFIERS", color=YELLOW))
    for key, d in DIFFICULTY_PRESETS.items():
        lines.append(f"  • {BOLD}{d['badge']}:{RESET} Death Save DC {d['death_save_dc']} | Rests: {d['rest_type']}")
        lines.append(f"    {DIM}{d['description']}{RESET}")

    # 5. Global Character Vault & Party Builder
    lines.append(box_section(f"🧙 GLOBAL CHARACTER VAULT ({len(vault_chars)} Heroes Available)", color=BRIGHT_YELLOW))
    active_party_ids = set(active_manifest.get("party_ids", [])) if active_manifest else set()
    
    if vault_chars:
        for c in vault_chars[:8]:
            cid = c.get("id")
            in_party = cid in active_party_ids
            status_tag = f"{BRIGHT_GREEN}[IN PARTY]{RESET}" if in_party else f"{DIM}[BENCH]{RESET}"
            c_name = c.get("name", "Hero")
            c_cls = c.get("class", "Adventurer")
            c_lvl = c.get("level", 1)
            c_spec = c.get("species", "Human")
            hp_cur = c.get("hp", {}).get("current", 10)
            hp_max = c.get("hp", {}).get("max", 10)
            lines.append(f"  {status_tag} {BOLD}{c_name}{RESET} (Lvl {c_lvl} {c_spec} {c_cls}) — {hp_cur}/{hp_max} HP (ID: `{cid}`)")
    else:
        lines.append(f"  {DIM}Character vault is empty. Create a hero with 'python dnd.py create-character'{RESET}")

    # 6. Action Commands
    lines.append(box_section("🎮 RUN SETUP COMMANDS", color=GREEN))
    lines.append(f"  {BOLD}1. Create New Run{RESET}   : {CYAN}python dnd.py run new --name \"<name>\" --difficulty normal|hardcore|story{RESET}")
    lines.append(f"  {BOLD}2. Switch Run{RESET}       : {CYAN}python dnd.py run switch <run_id>{RESET}")
    lines.append(f"  {BOLD}3. Add to Party{RESET}     : {CYAN}python dnd.py party add <character_id>{RESET}")
    lines.append(f"  {BOLD}4. Remove Party{RESET}    : {CYAN}python dnd.py party remove <character_id>{RESET}")
    lines.append(f"  {BOLD}5. Enter Field / Play{RESET}: {CYAN}python dnd.py menu{RESET} or {CYAN}python dnd.py play \"<action>\"{RESET}")

    lines.append("\n" + "=" * width + "\n")
    return "\n".join(lines)
