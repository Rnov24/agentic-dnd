# Plan 008: Compendium Schema Validator & Homebrew Linter

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.

## Status

- **Priority**: P1
- **Effort**: S (1–2 hours)
- **Risk**: LOW
- **Depends on**: none
- **Category**: dx / tooling
- **Planned at**: 2026-08-20

## Why this matters

Modders and developers adding homebrew classes, species, backgrounds, spells, monsters, or magic items currently have no automated tool to validate JSON schemas or detect missing required fields (e.g. missing spell school, invalid hit die, missing damage formula) before runtime. A dedicated compendium validator and linter CLI ensures rules compendiums remain structurally sound and compliant.

## Current state

- `tools/compendium.py`: Provides getters for all compendiums in `rules/*.json`, but lacks a validation and diagnostics engine.
- `rules/`: Contains `classes.json`, `species.json`, `backgrounds.json`, `presets.json`, `progression.json`, `encounters.json`, `actions.json`, `conditions.json`, `spells.json`, `monsters.json`, `magic_items.json`, `treasure.json`, and `defaults.json`.

## Scope

**In scope**:
- `tools/compendium_validator.py` (Create validator class checking schema compliance and stats for all 13 compendiums)
- `dnd.py` (Add `compendium` subcommand: `python dnd.py compendium [validate/stats/list]`)
- `tests/test_compendium_validator.py` (Unit tests verifying compendium validation passes for current rules and detects synthetic errors)

**Out of scope**:
- Do not modify immutable compendium data in `rules/*.json`.

## Step-by-Step Implementation

### Step 1: Implement `CompendiumValidator` in `tools/compendium_validator.py`
1. Validate required fields for:
   - Spells: `name`, `level`, `school`, `casting_time`, `range`, `components`, `duration`
   - Monsters: `name`, `cr`, `ac`, `hp`, `speed`, `stats`
   - Magic Items: `name`, `rarity`, `type`
   - Classes: `name`, `hit_die`, `primary_ability`, `saving_throw_proficiencies`
   - Species: `name`, `size`, `speed`
2. `get_stats()`: Return counts of all registered compendium entities.

### Step 2: Register `compendium` command in `dnd.py`
Add `cmd_compendium` and `p_comp` subparser in `dnd.py`.

### Step 3: Write tests in `tests/test_compendium_validator.py`
Test that current rules pass validation with zero errors.

## Verification Gate
Run:
```bash
python -m unittest tests/test_compendium_validator.py
python dnd.py compendium validate
python dnd.py test
```

## STOP Conditions
- If any existing compendium fails validation, check whether a field is genuinely required or optional.
