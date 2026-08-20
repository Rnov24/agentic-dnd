# Plan 009: Modular Adventure Package Scaffolder

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
- **Category**: dx / feature
- **Planned at**: 2026-08-20

## Why this matters

Creating a new modular campaign or adventure package currently requires manually creating a directory structure with 8+ subfolders (`locations/`, `npcs/`, `quests/`, `items/`, `monsters/`, `encounters/`, `factions/`, `chapters/`) and authoring `adventure.json` from scratch. Providing an automated scaffolding CLI (`python dnd.py adventure new <slug> --title <title>`) streamlines adventure creation for DMs and modders.

## Current state

- `tools/adventure_loader.py`: Has `list_adventures()`, `validate_adventure()`, and `load_adventure_into_campaign()`, but no `scaffold_adventure()`.
- `adventures/lost_mine_of_phandelver/`: Reference modular adventure package layout.

## Scope

**In scope**:
- `tools/adventure_loader.py` (Add `scaffold_adventure(slug, title, levels, author)`)
- `dnd.py` (Add `new` action to `adventure` subparser: `python dnd.py adventure new <slug> [--title <title>]`)
- `tests/test_adventure_loader.py` (Unit tests verifying folder structure and manifest generation)

**Out of scope**:
- Do not modify existing `lost_mine_of_phandelver` package.

## Step-by-Step Implementation

### Step 1: Implement `scaffold_adventure` in `tools/adventure_loader.py`
Create directories:
- `adventures/<slug>/`
- Subdirectories: `locations/`, `npcs/`, `quests/`, `items/`, `monsters/`, `encounters/`, `factions/`, `chapters/`, `lore/`
- Default boilerplate files: `adventure.json`, `README.md`, `locations/locations.json`, `npcs/npcs.json`, `quests/quests.json`, `items/magic_items.json`, `monsters/monsters.json`, `encounters/encounters.json`, `factions/factions.json`.

### Step 2: Wire CLI action `new` into `dnd.py`
Update `cmd_adventure` to handle `action == "new"`.

### Step 3: Add unit tests in `tests/test_adventure_loader.py`
Verify that `scaffold_adventure` creates a package that passes `validate_adventure`.

## Verification Gate
Run:
```bash
python -m unittest tests/test_adventure_loader.py
python dnd.py test
```

## STOP Conditions
- If scaffolding an adventure with an existing slug, return an error rather than overwriting without explicit force flag.
