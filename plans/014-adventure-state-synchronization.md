# Plan 014: Full Adventure Lifecycle State Synchronization

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.

## Status

- **Priority**: P1
- **Effort**: S (1 hour)
- **Risk**: LOW
- **Depends on**: 013
- **Category**: persistence / state
- **Planned at**: 2026-08-20

## Why this matters

When an adventure module is loaded (`python dnd.py adventure load <slug>`), `AdventureLoader` currently copies only `npcs`, `quests`, and `factions` to `state/`. It omits `items`, `monsters`, `encounters`, and `locations`. Synchronizing all adventure assets ensures the persistent state and campaign documents are fully populated and inspectable.

## Current state

- `tools/adventure_loader.py:load_adventure_into_campaign`: Synchronizes only a subset of JSONs.
- `tools/state_manager.py`: Lacks convenience getters for active campaign items, locations, and encounters.

## Scope

**In scope**:
- `tools/adventure_loader.py` (Synchronize `items/magic_items.json` -> `state/items.json`, `monsters/monsters.json` -> `state/monsters.json`, `encounters/encounters.json` -> `state/encounters.json`, `locations/locations.json` -> `state/locations.json`)
- `tools/state_manager.py` (Add `get_items()`, `get_locations()`, `get_encounters()`)
- `tests/test_adventure_loader.py` (Add unit test verifying all 7 domain files are synchronized on load)

**Out of scope**:
- Do not remove existing backward-compatible methods in `StateManager`.

## Step-by-Step Implementation

### Step 1: Update `state_mappings` in `tools/adventure_loader.py`
Add mappings for:
- `("items/magic_items.json", "items.json")`
- `("monsters/monsters.json", "monsters.json")`
- `("encounters/encounters.json", "encounters.json")`
- `("locations/locations.json", "locations.json")`

### Step 2: Add getters to `tools/state_manager.py`
Add `get_items()`, `get_locations()`, `get_encounters()` with fallback to empty dicts/lists.

### Step 3: Add unit test in `tests/test_adventure_loader.py`
Verify that loading *Lost Mine of Phandelver* creates `items.json`, `monsters.json`, `encounters.json`, and `locations.json` in `state/`.

## Verification Gate
Run:
```bash
python -m unittest tests/test_adventure_loader.py
python dnd.py test
```

## STOP Conditions
- If an adventure package lacks one of the optional files (e.g. no custom monsters), skip gracefully without raising errors.
