# Plan 001: Fix StateManager save_relationships for Rollback Integrity

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**: Inspect lines 150–210 in `tools/state_manager.py` and line 172 in `tools/git_versioning.py`.
> If any in-scope file changed unexpectedly, treat it as a STOP condition.

## Status

- **Priority**: P1
- **Effort**: S (< 1 hour)
- **Risk**: LOW
- **Depends on**: none
- **Category**: bug
- **Planned at**: 2026-08-20

## Why this matters

When rolling back campaign history using `python dnd.py rollback <commit_id>`, `CampaignGitManager.rollback()` attempts to restore all state domains present in the snapshot. If the snapshot contains a `"relationships"` domain, it invokes `sm.save_relationships()`. Because `StateManager` currently lacks `save_relationships`, `get_relationships`, and `state/relationships.json` management, the rollback crashes with an unhandled `AttributeError`, corrupting the recovery workflow.

## Current state

- Relevant files:
  - `tools/git_versioning.py:171-173` — calls `sm.save_relationships(target_state["relationships"])`
  - `tools/state_manager.py:50-70, 160-205` — manages `world.json`, `party.json`, `combat.json`, `npcs.json`, `quests.json`, but lacks `relationships.json`.
  - `rules/defaults.json:21-23` — already specifies default `"relationships": {"relationships": []}`.

### Code Excerpt (`tools/git_versioning.py:161-173`)
```python
if "world" in target_state:
    sm.save_world(target_state["world"])
if "party" in target_state:
    sm.save_party(target_state["party"])
if "npcs" in target_state:
    sm.save_npcs(target_state["npcs"])
if "combat" in target_state:
    sm.save_combat(target_state["combat"])
if "quests" in target_state:
    sm.save_quests(target_state["quests"])
if "relationships" in target_state:
    sm.save_relationships(target_state["relationships"])
```

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Run Unit Tests | `python dnd.py test` | 97+ tests passed, exit 0 |
| Verify Rollback | `python -m unittest tests/test_git_versioning.py` | OK, exit 0 |

## Scope

**In scope**:
- `tools/state_manager.py` (Add `relationships_file`, `get_relationships`, `save_relationships`, `update_relationships`)
- `tests/test_git_versioning.py` (Add test case for rollback with relationships domain)

**Out of scope**:
- Do not modify snapshot serialization format in `tools/git_versioning.py`.
- Do not modify `rules/defaults.json`.

## Step-by-Step Implementation

### Step 1: Add relationships file initialization to `StateManager`
In `tools/state_manager.py`:
1. In `__init__`: Add `self.relationships_file = self.state_dir / "relationships.json"`.
2. In `_init_files`: Add:
```python
if not self.relationships_file.exists():
    default_rel = self.compendium.get_defaults("relationships")
    self._save_json(self.relationships_file, default_rel)
```

### Step 2: Implement relationships accessors in `StateManager`
Add the following methods to `StateManager`:
```python
def get_relationships(self) -> Dict[str, Any]:
    return self._load_json(self.relationships_file)

def save_relationships(self, relationships_data: Dict[str, Any]) -> None:
    self._save_json(self.relationships_file, relationships_data)

def update_relationships(self, relationships_data: Dict[str, Any]) -> bool:
    self._save_json(self.relationships_file, relationships_data)
    return True
```
Also update `get_full_state()` to include `"relationships": self.get_relationships()`.

### Step 3: Add test in `tests/test_git_versioning.py`
Add a test method `test_rollback_with_relationships` verifying that committing state with a `"relationships"` key and rolling back restores `state/relationships.json` without error.

## Verification Gate
Run:
```bash
python -m unittest tests/test_git_versioning.py
python dnd.py test
```
Confirm all tests pass with code 0.

## STOP Conditions
- If `tests/test_git_versioning.py` fails on other existing tests, STOP and review diff.
