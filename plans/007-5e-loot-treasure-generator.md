# Plan 007: Deterministic 5e Loot & Treasure Hoard Generator

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.

## Status

- **Priority**: P3
- **Effort**: S (half day)
- **Risk**: LOW
- **Depends on**: none
- **Category**: direction / feature
- **Planned at**: 2026-08-20

## Why this matters

When an encounter concludes or players discover a chest, DMs currently determine loot manually or invent values. D&D 5e defines deterministic individual and hoard treasure tables by Challenge Rating (CR 0–4, CR 5–10, CR 11–16, CR 17+), rolling coin distributions (CP, SP, EP, GP, PP), gems/art objects, and magic item tables. Providing a deterministic loot generator allows AI DMs and players to award balanced, rules-compliant rewards.

## Current state

- `rules/encounters.json`: Contains CR matrices and encounter thresholds.
- `rules/magic_items.json`: Compendium of magic items with rarity and attunement.
- `tools/encounters.py`: Calculates encounter difficulty, but does not calculate loot drops.

## Scope

**In scope**:
- `rules/treasure.json` (Create table of individual and hoard treasure rolls by CR tier: 0-4, 5-10, 11-16, 17+)
- `tools/loot.py` (Create `LootGenerator` with `generate_individual_treasure(cr, seed)` and `generate_hoard_treasure(cr, seed)`)
- `dnd.py` (Add CLI command `python dnd.py loot [--cr <num>] [--hoard] [--seed <num>]`)
- `tests/test_loot.py` (Unit tests verifying coin generation, gem valuation, and magic item selection)

**Out of scope**:
- Do not modify party inventory automatically unless explicitly passed `--distribute` or `--add-to-party`.

## Step-by-Step Implementation

### Step 1: Create `rules/treasure.json`
Define standard tables for CR tiers 0–4 and 5–10 with coin formulas (e.g. `3d6 CP`, `1d6 GP`) and magic item table rolls.

### Step 2: Implement `tools/loot.py`
```python
class LootGenerator:
    def __init__(self, project_root: Optional[str] = None):
        self.compendium = Compendium.get_instance(project_root)
        
    def generate_individual(self, cr: float, seed: Optional[int] = None) -> Dict[str, Any]:
        ...
        
    def generate_hoard(self, cr: float, seed: Optional[int] = None) -> Dict[str, Any]:
        ...
```

### Step 3: Register `loot` subcommand in `dnd.py`
Add `p_loot` subcommand in `dnd.py`.

### Step 4: Write Unit Tests in `tests/test_loot.py`
Verify deterministic output with fixed seed and proper coin scaling.

## Verification Gate
Run:
```bash
python -m unittest tests/test_loot.py
python dnd.py test
```

## STOP Conditions
- If magic item generation fails to find an item for a given rarity, fall back to a random item of matching rarity from `rules/magic_items.json`.
