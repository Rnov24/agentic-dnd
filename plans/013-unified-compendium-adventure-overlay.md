# Plan 013: Unified Multi-Tier Compendium & Asset Overlay

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
- **Category**: architecture / compendium
- **Planned at**: 2026-08-20

## Why this matters

Currently, `Compendium` (`tools/compendium.py`), `tools/magic_items.py`, and `tools/monsters.py` read only from `rules/*.json`. They have no awareness of active adventure packages (e.g. `adventures/lost_mine_of_phandelver/` containing *Spider Staff*, *Staff of Defense*, *Nezznar*, *Nothic*, *Redbrand Ruffian*). As a result, querying adventure assets fails with `"Not found"`. Implementing a multi-tier overlay architecture allows all runtime tools to seamlessly discover and query both Core Rules and active Adventure assets.

## Current state

- `tools/compendium.py`: Queries only `rules/`.
- `adventures/lost_mine_of_phandelver/items/magic_items.json`: Has adventure-specific magic items (*Spider Staff*, *Staff of Defense*, *Lightbringer*, *Dragonguard*).
- `adventures/lost_mine_of_phandelver/monsters/monsters.json`: Has adventure-specific monsters (*Nezznar*, *Nothic*, *Redbrand Ruffian*, *Evil Mage*, *Goblin Boss*).

## Scope

**In scope**:
- `tools/compendium.py` (Add active adventure detection and multi-tier resolution for `get_magic_item`, `get_magic_items`, `get_monster`, `get_monsters`, `get_location`, `get_encounter`)
- `tools/magic_items.py` (Forward item lookups through `Compendium` with source attribution)
- `dnd.py:cmd_item` and `dnd.py:cmd_monster` (Display source attribution badge: `[Core 5e Basic Rules]` vs `[Adventure: Lost Mine of Phandelver]`)
- `tests/test_compendium_overlay.py` (Unit tests verifying multi-tier item and monster resolution)

**Out of scope**:
- Do not modify raw `rules/*.json` static compendiums.

## Step-by-Step Implementation

### Step 1: Add Active Adventure Resolution in `tools/compendium.py`
1. Detect active adventure from `state/world.json` (`campaign_id`).
2. If `campaign_id` exists, check `adventures/<campaign_id>/` for:
   - `items/magic_items.json`
   - `monsters/monsters.json`
   - `locations/locations.json`
   - `encounters/encounters.json`
3. Merge adventure assets as an overlay on top of core rules assets, tagging each entity with `_source` (`"core"` or `"adventure:<campaign_id>"`).

### Step 2: Update `tools/magic_items.py` and `dnd.py`
Use the overlay resolver for `get_magic_item()` and `get_monster()`. Render the source badge in CLI output.

### Step 3: Write tests in `tests/test_compendium_overlay.py`
Verify that core items and adventure items (*Spider Staff*, *Staff of Defense*, *Nezznar*, *Nothic*) are resolved seamlessly.

## Verification Gate
Run:
```bash
python -m unittest tests/test_compendium_overlay.py
python dnd.py item "Spider Staff"
python dnd.py monster "Nezznar"
python dnd.py test
```

## STOP Conditions
- If an adventure item has the same ID as a core item, the adventure item takes precedence as a local overlay.
