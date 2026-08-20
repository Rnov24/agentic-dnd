# Plan 004: Dynamic Entity and Weapon Resolution in Rules Agent

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**: Inspect `agents/rules.py:25-50` and `agents/orchestrator.py:165-175`.

## Status

- **Priority**: P2
- **Effort**: S–M (half day)
- **Risk**: LOW
- **Depends on**: none
- **Category**: tech-debt / architecture
- **Planned at**: 2026-08-20

## Why this matters

The `RulesAgent` and `OrchestratorAgent` currently contain legacy hardcoded entity defaults (e.g. `target_name = "guard_karl"`, `weapon = "Black Glass Dagger"`). In custom or modular adventures like *Lost Mine of Phandelver*, when an actor attacks a goblin or bugbear with a longsword, the system may fall back to `"guard_karl"` or `"Black Glass Dagger"` if no explicit match is triggered, causing immersion dissonance and inaccurate weapon damage math.

## Current state

- `agents/rules.py:28-29`:
```python
target_name = "guard_karl" if "karl" in lower_intent or "guard" in lower_intent else ("captain_aldric" if "aldric" in lower_intent else "enemy")
weapon = "Black Glass Dagger" if "dagger" in lower_intent or "black glass" in lower_intent else ("Shortbow" if "bow" in lower_intent or "shoot" in lower_intent else "Black Glass Dagger")
```
- `agents/orchestrator.py:166-168`:
```python
target_npc = self.state_manager.get_npc(rules_analysis.get("target", "guard_karl")) or {
    "name": "Guard Karl", "ac": 14, "hp": {"current": 16, "max": 16}
}
```

## Commands you will need

| Purpose | Command | Expected on success |
|---|---|---|
| Test Multi-Agent Intent | `python -m unittest tests/test_multi_agent_flow.py` | OK, exit 0 |
| Run Full Test Suite | `python dnd.py test` | 97+ tests passed, exit 0 |

## Scope

**In scope**:
- `agents/rules.py` (Implement dynamic target matching against `context.get("threats")` and `npcs.json`; dynamic weapon matching against `actor.attacks` and `actor.equipment`)
- `agents/orchestrator.py` (Refactor fallback target lookup to query active room threats / monsters / NPCs instead of static Karl dictionary)

**Out of scope**:
- Do not modify monster compendiums in `rules/monsters.json`.

## Step-by-Step Implementation

### Step 1: Implement dynamic weapon matching in `agents/rules.py`
Add weapon extraction helper that checks `actor.get("attacks")` and `actor.get("equipment")`:
- If actor has `Quarterstaff`, `Dagger`, `Longsword`, match whichever weapon is mentioned in intent.
- Default to actor's primary weapon in `actor.get("attacks", [{}])[0]` instead of a hardcoded dagger string.

### Step 2: Implement dynamic target resolution in `agents/rules.py` and `agents/orchestrator.py`
1. Extract potential target names from `context.get("threats", [])` (e.g. `"Cragmaw Goblin"`, `"Bugbear"`) and `npcs` in area.
2. In `OrchestratorAgent`, if target is a monster (e.g. `"goblin"`), look up the monster statblock via `Compendium.get_instance().get_monster(target_name)` if not found in `npcs.json`.

### Step 3: Verify with unit tests
Run `python -m unittest tests/test_multi_agent_flow.py` and ensure existing tests still pass.

## Verification Gate
Run:
```bash
python -m unittest tests/test_multi_agent_flow.py
python dnd.py test
```

## STOP Conditions
- Ensure `test_attack_intent_orchestration` in `tests/test_multi_agent_flow.py` continues to pass without breaking backward compatibility for test fixtures.
