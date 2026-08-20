"""
Agentic D&D Interactive Command-Line Interface.
Provides interactive D&D gameplay, fast-boot HUD dashboards, and multi-agent execution traces.
"""

import sys
import time
from pathlib import Path

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
from tools.multiplayer import MultiplayerManager
from tools.character_inspector import CharacterInspector
from tools.menu import render_game_menu, get_boot_context


def main():
    orch = OrchestratorAgent(str(PROJECT_ROOT))
    sm = StateManager(str(PROJECT_ROOT))
    git = CampaignGitManager(str(PROJECT_ROOT))
    dev = DeveloperAgent(str(PROJECT_ROOT))
    mp = MultiplayerManager(str(PROJECT_ROOT))
    insp = CharacterInspector(str(PROJECT_ROOT))

    print("\n" + render_game_menu(project_root=str(PROJECT_ROOT)))
    current_mode = "GAME_MODE"

    while True:
        try:
            active_char = mp.get_active_player() or {}
            char_name = active_char.get("name", "Adventurer")
            prompt_label = f"[{current_mode} | {char_name}] > "
            user_input = input(prompt_label).strip()
            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit", "/exit", "/quit"]:
                print("Farewell, adventurer.")
                break

            if user_input.lower() in ["/menu", "menu", "/dashboard", "10"]:
                print("\n" + render_game_menu(project_root=str(PROJECT_ROOT)))
                continue

            if user_input.lower() == "/help":
                print("""
Available Commands:
  /menu         Display the full game dashboard and action menu
  /inspect      Inspect active character profile, stats, spells & equipment
  /party        List party roster and active player
  /switch <id>  Switch active player character
  /mode         Toggle between GAME_MODE and DEVELOPER_MODE
  /history      View Git commit timeline
  /rollback <id>Rollback state to snapshot
  /tests        Run automated Python test suite
  /status       Display party & scene status
  /exit         Exit the CLI
""")
                continue

            if user_input.lower().startswith("/switch") or user_input.lower().startswith("switch"):
                parts = user_input.split(maxsplit=1)
                if len(parts) < 2:
                    print("Usage: /switch <character_name_or_id>")
                else:
                    res = mp.set_active_player(parts[1])
                    if res.get("success"):
                        print(f"▶ Switched active player to: {res['active_character'].get('name')}")
                    else:
                        print(f"Error: {res.get('error')}")
                continue

            if user_input.lower() in ["/inspect", "inspect", "6"]:
                print(insp.format_character_sheet(active_char))
                continue

            if user_input.lower() in ["/party", "party", "7"]:
                for p in mp.get_party():
                    hp = p.get("hp", {})
                    active_marker = "▶ " if p.get("id") == active_char.get("id") else "  "
                    print(f"{active_marker}{p.get('name')} (Lvl {p.get('level', 1)} {p.get('class', 'Fighter')}) - HP {hp.get('current')}/{hp.get('max')}")
                continue

            if user_input.lower() == "/mode":
                if current_mode == "GAME_MODE":
                    current_mode = "DEVELOPER_MODE"
                    print("Switched to DEVELOPER_MODE (Privileged Developer Authority)")
                else:
                    current_mode = "GAME_MODE"
                    print("Switched to GAME_MODE (Sandboxed Player Authority)")
                continue

            if user_input.lower() == "/history":
                timeline = git.get_history_timeline()
                print("\n=== Git Campaign History Timeline ===")
                for c in timeline[:8]:
                    print(f"Commit [{c['commit_id']}] [{c['timestamp']}] | {c['agent']}: {c['intent']}")
                print()
                continue

            if user_input.lower().startswith("/rollback"):
                parts = user_input.split()
                if len(parts) < 2:
                    print("Usage: /rollback <commit_id>")
                else:
                    cid = parts[1]
                    res = git.rollback(cid)
                    if res:
                        print(f"Successfully rolled back to commit {cid}!")
                    else:
                        print(f"Rollback failed: commit {cid} not found.")
                continue

            if user_input.lower() == "/tests":
                print("Running test suite...")
                test_res = dev.run_tests()
                print(test_res["output"])
                continue

            if user_input.lower() == "/status":
                world = sm.get_world()
                print(f"\nLocation: {world.get('active_location')}")
                print(f"Weather: {world.get('weather')}")
                print(f"Party:")
                for p in sm.get_party():
                    hp = p.get("hp", {})
                    print(f" - {p.get('name')}: HP {hp.get('current')}/{hp.get('max')}, AC {p.get('ac')}")
                print()
                continue

            # Process natural language intent
            print(f"\n-> Orchestrator analyzing intent...")
            trace = orch.process_player_intent(user_input, character_id=active_char.get("id"))

            for step in trace.steps:
                agent = step.agent
                print(f"  -> [{agent}] {step.action}")
                if "formula" in step.details:
                    print(f"     Formula: {step.details['formula']}")

            if trace.requires_approval:
                print(f"\n==================== CONSEQUENTIAL CHANGE APPROVAL ====================")
                print(f"  Action: {trace.approval_payload.get('action')}")
                print(f"  Cause:  {trace.approval_payload.get('cause')}")
                print(f"  Affected: {', '.join(trace.approval_payload.get('affected_files', []))}")
                print(f"=======================================================================")
                ans = input("Approve this consequential change? [y/N]: ").strip().lower()
                if ans == "y":
                    git.commit(
                        full_state=sm.get_full_state(),
                        intent=user_input,
                        reason=f"Approved: {trace.approval_payload.get('action')}",
                        agent="Player Approval",
                    )
                    print("Change approved and committed.")
                else:
                    print("Change rejected. State preserved.")
                    continue

            print(f"\n[DM Narration]")
            print(trace.narration)
            print()

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()

