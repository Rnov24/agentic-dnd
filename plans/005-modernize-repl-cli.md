# Plan 005: Modernize Interactive REPL in cli.py

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**: Inspect `cli.py:1-60` and `tools/menu.py:50-100`.

## Status

- **Priority**: P2
- **Effort**: S (1 hour)
- **Risk**: LOW
- **Depends on**: none
- **Category**: tech-debt / dx
- **Planned at**: 2026-08-20

## Why this matters

The project has two CLI entry points: `dnd.py` (the official CLI Router and agent tool bridge with `menu`, `boot`, `play`, `party`, `inspect`, etc.) and `cli.py` (a legacy experimental REPL loop). `cli.py` currently hardcodes Aria Nightwind, bypasses `MultiplayerManager.get_active_player()`, and does not integrate `render_game_menu()`. Modernizing `cli.py` to wrap `tools/menu.py` and `dnd.py` gives players a cohesive, beautiful interactive terminal shell.

## Current state

- `cli.py:44-51`:
```python
current_mode = "GAME_MODE"
party = sm.get_party()
active_char = party[0] if party else {"name": "Aria Nightwind"}
print(f"[Active Character] {active_char.get('name')} | Level {active_char.get('level', 3)} {active_char.get('class', 'Rogue')}")
```

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Verify REPL Import & Syntax | `python -c "import cli"` | exit 0 |
| Run Full Test Suite | `python dnd.py test` | 97+ tests passed, exit 0 |

## Scope

**In scope**:
- `cli.py` (Refactor to use `render_game_menu()` on startup, dynamically resolve active character via `MultiplayerManager`, and support quick menu shortcuts [1–10])

**Out of scope**:
- Do not remove or alter `dnd.py`.

## Step-by-Step Implementation

### Step 1: Update `cli.py` initialization
In `cli.py`:
1. Import `render_game_menu` and `get_boot_context` from `tools.menu`.
2. Import `MultiplayerManager` from `tools.multiplayer`.
3. In `main()`, display `render_game_menu()` upon launch instead of the legacy text banner.

### Step 2: Handle numbered shortcuts in REPL loop
Allow player to input `1` through `10` or natural language text:
- `1` / natural language: runs `orch.process_player_intent(user_input)`
- `/menu`: renders `render_game_menu()`
- `/inspect`: invokes `CharacterInspector`
- `/switch <name>`: invokes `MultiplayerManager.set_active_player`
- `/help`: prints quick command reference

### Step 3: Verification
Run:
```bash
python -c "import cli; print('CLI module OK')"
python dnd.py test
```

## Verification Gate
Run `python dnd.py test` and confirm exit code 0.

## STOP Conditions
- If any keyboard interrupt or EOF handling breaks in terminal environments, preserve standard try/except loops.
