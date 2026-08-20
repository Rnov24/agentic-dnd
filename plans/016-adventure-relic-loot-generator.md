# Plan 016: Adventure-Specific Relic Drops in Loot Generator

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
- **Category**: loot / rewards
- **Planned at**: 2026-08-20

## Why this matters

The 5e loot generator (`tools/loot.py`) currently pulls magic items exclusively from `rules/magic_items.json`. When running an adventure module (e.g. *Lost Mine of Phandelver*), DMs and the DM agent should be able to roll dungeon hoards that can include unique adventure relics (*Spider Staff*, *Staff of Defense*, *Lightbringer*, *Dragonguard*) alongside standard magic items.

## Current state

- `tools/loot.py:generate_hoard_treasure`: Pulls from core `compendium.get_magic_items()`.

## Scope

**In scope**:
- `tools/loot.py` (Include adventure items in magic item pool when active or when `--adventure` specified)
- `dnd.py:cmd_loot` (Add `--adventure` flag and auto-detection of active campaign)
- `tests/test_loot.py` (Add unit test verifying adventure items can appear in hoard loot)

**Out of scope**:
- Do not modify coin generation dice math.

## Step-by-Step Implementation

### Step 1: Update `tools/loot.py`
Use `Compendium.get_magic_items()` (which now includes active adventure items via Plan 013 overlay). Allow filtering or weighting adventure relics.

### Step 2: Update `dnd.py:cmd_loot`
Pass adventure context to `LootGenerator`.

### Step 3: Add unit test in `tests/test_loot.py`
Verify that `LootGenerator` with active adventure includes adventure items in available magic items.

## Verification Gate
Run:
```bash
python -m unittest tests/test_loot.py
python dnd.py loot --cr 3 --hoard
python dnd.py test
```

## STOP Conditions
- Ensure determinism (`--seed`) is maintained when adventure items are present.
