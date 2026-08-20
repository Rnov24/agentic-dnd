"""
Visual Output Formatter & Terminal Styler for Agentic D&D.
Provides clean ANSI styling, visual health bars, structured cards,
dice roll badges, and Theater-of-the-Mind narrative panels.
"""

import sys
import os

# Check if colors should be enabled
USE_COLOR = os.environ.get("NO_COLOR") is None and hasattr(sys.stdout, "isatty") and sys.stdout.isatty()

# ANSI Color Codes
RESET = "\033[0m" if USE_COLOR else ""
BOLD = "\033[1m" if USE_COLOR else ""
DIM = "\033[2m" if USE_COLOR else ""
ITALIC = "\033[3m" if USE_COLOR else ""

# Foreground Colors
RED = "\033[31m" if USE_COLOR else ""
GREEN = "\033[32m" if USE_COLOR else ""
YELLOW = "\033[33m" if USE_COLOR else ""
BLUE = "\033[34m" if USE_COLOR else ""
MAGENTA = "\033[35m" if USE_COLOR else ""
CYAN = "\033[36m" if USE_COLOR else ""
WHITE = "\033[37m" if USE_COLOR else ""
BRIGHT_RED = "\033[91m" if USE_COLOR else ""
BRIGHT_GREEN = "\033[92m" if USE_COLOR else ""
BRIGHT_YELLOW = "\033[93m" if USE_COLOR else ""
BRIGHT_BLUE = "\033[94m" if USE_COLOR else ""
BRIGHT_MAGENTA = "\033[95m" if USE_COLOR else ""
BRIGHT_CYAN = "\033[96m" if USE_COLOR else ""


def render_hp_bar(current: int, max_hp: int, temp: int = 0, length: int = 15) -> str:
    """Renders a visual health bar: [████████░░░░░░░] 8/15 HP (+3 Temp)"""
    if max_hp <= 0:
        return "[----------------]"
    
    pct = max(0.0, min(1.0, current / max_hp))
    filled_len = int(round(length * pct))
    empty_len = length - filled_len

    if pct > 0.5:
        bar_color = BRIGHT_GREEN
    elif pct > 0.25:
        bar_color = BRIGHT_YELLOW
    else:
        bar_color = BRIGHT_RED

    bar = f"{bar_color}{'█' * filled_len}{DIM}{'░' * empty_len}{RESET}"
    temp_str = f" {CYAN}(+{temp} Temp){RESET}" if temp > 0 else ""
    return f"[{bar}] {BOLD}{current}/{max_hp}{RESET} HP{temp_str}"


def render_slot_pips(current: int, max_slots: int) -> str:
    """Renders spell slot charge pips: [●●○○] 2/4"""
    filled = "●" * current
    empty = "○" * (max_slots - current)
    return f"[{BRIGHT_CYAN}{filled}{DIM}{empty}{RESET}] {current}/{max_slots}"


def box_header(title: str, width: int = 65, color: str = BRIGHT_CYAN) -> str:
    """Creates a stylized header banner."""
    pad = width - len(title) - 4
    left = pad // 2
    right = pad - left
    border = "=" * width
    return f"{color}{border}\n  {' ' * left}{BOLD}{title.upper()}{RESET}{color}{' ' * right}  \n{border}{RESET}"


def box_section(title: str, color: str = YELLOW) -> str:
    """Creates a section break header."""
    return f"\n{color}--- [ {BOLD}{title}{RESET}{color} ] ---{RESET}"


def badge(text: str, bg_type: str = "info") -> str:
    """Returns a styled inline badge (SUCCESS, FAILURE, CRIT, etc.)."""
    if bg_type == "success":
        return f"{BRIGHT_GREEN}[✓ {text}]{RESET}"
    elif bg_type == "failure":
        return f"{BRIGHT_RED}[✗ {text}]{RESET}"
    elif bg_type == "crit":
        return f"{BRIGHT_YELLOW}{BOLD}[★ {text} ★]{RESET}"
    elif bg_type == "warn":
        return f"{BRIGHT_YELLOW}[! {text}]{RESET}"
    elif bg_type == "active":
        return f"{BRIGHT_CYAN}[▶ {text}]{RESET}"
    else:
        return f"{WHITE}[{text}]{RESET}"


def format_dialogue(speaker: str, text: str, role: str = "") -> str:
    """Formats NPC or companion dialogue with rich styling."""
    role_str = f" {DIM}({role}){RESET}" if role else ""
    return f"{BRIGHT_MAGENTA}💬 {BOLD}{speaker}{RESET}{role_str}: \"{ITALIC}{text}{RESET}\""


def format_dm_narration(narration: str) -> str:
    """Formats DM Theater-of-the-Mind narration panel."""
    lines = narration.strip().split("\n")
    formatted_lines = []
    for line in lines:
        if line.startswith("> "):
            formatted_lines.append(f"  {BRIGHT_BLUE}│{RESET} {line[2:]}")
        else:
            formatted_lines.append(f"  {line}")
    return "\n".join(formatted_lines)


def render_state_diff(diff_data: dict) -> str:
    """Formats a visual high-contrast before/after state diff card."""
    lines = []
    lines.append(box_header("CAMPAIGN STATE DIFF", width=70, color=BRIGHT_YELLOW))
    has_diff = False
    for domain, changes in diff_data.items():
        if not changes:
            continue
        has_diff = True
        lines.append(box_section(domain.upper(), color=CYAN))
        if isinstance(changes, dict):
            for k, change in changes.items():
                if isinstance(change, dict) and "before" in change and "after" in change:
                    lines.append(f"  • {BOLD}{k}{RESET}: {BRIGHT_RED}-{change['before']}{RESET} -> {BRIGHT_GREEN}+{change['after']}{RESET}")
                elif isinstance(change, dict) and "added" in change:
                    lines.append(f"  {BRIGHT_GREEN}+ [ADDED]{RESET} {k}: {change['added']}")
                elif isinstance(change, dict) and "removed" in change:
                    lines.append(f"  {BRIGHT_RED}- [REMOVED]{RESET} {k}: {change['removed']}")
                else:
                    lines.append(f"  • {k}: {change}")
        elif isinstance(changes, list):
            for item in changes:
                lines.append(f"  • {item}")
        else:
            lines.append(f"  • {changes}")
    if not has_diff:
        lines.append(f"  {DIM}No state mutations recorded in this commit.{RESET}")
    lines.append("")
    return "\n".join(lines)


def render_turn_mini_hud(
    actor: dict,
    world_state: dict = None,
    combat_state: dict = None
) -> str:
    """Renders a compact tactical status HUD for post-turn feedback."""
    name = actor.get("name", "Hero")
    cls_name = actor.get("class", "Adventurer")
    lvl = actor.get("level", 1)
    hp = actor.get("hp", {})
    cur_hp = hp.get("current", 10)
    max_hp = hp.get("max", 10)
    temp_hp = hp.get("temp", 0) or 0
    hp_badge = render_hp_bar(cur_hp, max_hp, temp_hp, length=8)
    
    conds = actor.get("conditions", [])
    cond_str = f" | {BRIGHT_YELLOW}{' '.join(f'[{c}]' for c in conds)}{RESET}" if conds else ""
    
    loc = world_state.get("active_location", "") if world_state else ""
    loc_str = f" | {DIM}Loc:{RESET} {loc}" if loc else ""

    border = "─" * 70
    return f"{DIM}{border}{RESET}\n  {BRIGHT_CYAN}▶ TURN HUD:{RESET} {BOLD}{name}{RESET} (Lvl {lvl} {cls_name}) | {hp_badge}{cond_str}{loc_str}\n{DIM}{border}{RESET}"


def render_mechanics_audit_card(
    title: str,
    breakdown_lines: list,
    outcome: str,
    is_success: bool = True
) -> str:
    """Renders a structured mathematical explanation card for checks, attacks, or damage."""
    color = BRIGHT_GREEN if is_success else BRIGHT_RED
    lines = [
        f"┌── {BOLD}{title}{RESET} " + "─" * max(4, 55 - len(title)),
    ]
    for b in breakdown_lines:
        lines.append(f"│  • {b}")
    lines.append(f"├── Outcome: {color}{BOLD}{outcome}{RESET}")
    lines.append("└" + "─" * 60)
    return "\n".join(lines)
