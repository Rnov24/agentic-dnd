# Plan 015: Adventure-Aware Encounter & Preset Calculator

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.

## Status

- **Priority**: P2
- **Effort**: S (1 hour)
- **Risk**: LOW
- **Depends on**: 013, 014
- **Category**: combat / encounters
- **Planned at**: 2026-08-20

## Why this matters

The D&D basic rules encounter calculator (`tools/encounters.py` and `dnd.py encounter`) currently requires typing monster names manually (e.g. `python dnd.py encounter -m "goblin,goblin"`). Curated adventure books provide pre-balanced encounters with specific tactics (e.g. *Goblin Ambush*, *Chieftain Klarg and Ripper*, *Venomfang*). Adding support for `--preset <id>` directly evaluates curated adventure encounters.

## Current state

- `dnd.py:cmd_encounter`: Accepts `--monsters` and `--party` but no `--preset`.
- `adventures/lost_mine_of_phandelver/encounters/encounters.json`: Contains pre-balanced encounters with tactics, base XP, and adjusted XP.

## Scope

**In scope**:
- `tools/encounters.py` (Add `get_adventure_encounters()` and `evaluate_preset_encounter()`)
- `dnd.py:cmd_encounter` (Add `--preset` argument and display tactics and difficulty)
- `tests/test_encounters.py` (Unit tests for preset evaluation)

**Out of scope**:
- Do not alter the underlying DMG XP multiplier math.

## Step-by-Step Implementation

### Step 1: Add preset encounter evaluation in `tools/encounters.py`
Load preset from `Compendium` or `state/encounters.json`. Calculate difficulty against active party levels.

### Step 2: Update `dnd.py:cmd_encounter`
Add `--preset` option. When specified, print encounter name, monsters breakdown, tactics, and difficulty.

### Step 3: Add unit tests in `tests/test_encounters.py`
Verify evaluation of `"goblin_ambush"` and `"klargs_den"`.

## Verification Gate
Run:
```bash
python -m unittest tests/test_encounters.py
python dnd.py encounter --preset goblin_ambush
python dnd.py test
```

## STOP Conditions
- If preset is not found, suggest available presets from active adventure.
