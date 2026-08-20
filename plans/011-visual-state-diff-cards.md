# Plan 011: Visual Before/After State Diff Cards

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.

## Status

- **Priority**: P2
- **Effort**: S (1 hour)
- **Risk**: LOW
- **Depends on**: none
- **Category**: ux / dx
- **Planned at**: 2026-08-20

## Why this matters

The `python dnd.py diff <commit_id>` command allows players and developers to inspect what changed in a turn. Currently, `dnd.py diff` prints a raw JSON dump or plain key listings. Rendering high-contrast ANSI diff cards (green `+` for gained HP/items, red `-` for damage taken/expended spell slots) turns timeline debugging into an intuitive, visual experience.

## Current state

- `tools/git_versioning.py:compute_diff`: Computes before/after state diff dictionaries.
- `dnd.py:cmd_diff`: Prints `json.dumps(diff, indent=2)`.

## Scope

**In scope**:
- `tools/formatting.py` (Add `render_state_diff(diff_data: Dict[str, Any]) -> str`)
- `dnd.py:cmd_diff` (Use `render_state_diff` for human terminal output)
- `tests/test_formatting.py` (Add unit test for diff card rendering)

**Out of scope**:
- Do not modify internal snapshot storage in `tools/git_versioning.py`.

## Step-by-Step Implementation

### Step 1: Add `render_state_diff` in `tools/formatting.py`
Render a formatted box showing:
- Header: `=== 🔄 STATE DIFF: Commit A -> Commit B ===`
- Section per changed domain (`world`, `party`, `combat`, `npcs`, `quests`, `relationships`)
- Added/modified fields in green `(+)` and removed/previous values in red `(-)`

### Step 2: Update `cmd_diff` in `dnd.py`
When `--json` is false, print `render_state_diff(diff)`.

### Step 3: Add unit test in `tests/test_formatting.py`
Test `render_state_diff` produces expected header and color tags.

## Verification Gate
Run:
```bash
python -m unittest tests/test_formatting.py
python dnd.py test
```

## STOP Conditions
- Ensure `python dnd.py diff <commit_id> --json` continues to output pure parseable JSON.
