# Plan 017: Typed Domain Models and Explicit Schema Contracts

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.

## Status

- **Priority**: P1
- **Effort**: M (0.5–1 day)
- **Risk**: LOW
- **Depends on**: none
- **Category**: tech-debt / architecture
- **Planned at**: commit `v1.0.0-phase4`, 2026-08-20

## Why this matters

The codebase currently relies almost entirely on loosely typed dictionaries (`Dict[str, Any]`) passed across agents, persistence boundaries, and tools. When keys change or vary slightly (e.g. `hp.current` vs `current_hp`, `is_player` vs `is_pc`, `armor_class` vs `ac`), errors fail silently by returning default values rather than surfacing schema mismatches. Creating a centralized typed domain models module (`tools/models.py`) with dataclasses for `Character`, `Monster`, `MagicItem`, `Spell`, `EncounterPreset`, and `Location` provides explicit schema contracts and eliminates data ambiguity.

## Current state

- Untyped dictionary navigation across all agents and tools:
  - `agents/orchestrator.py:96-107`: `party[0].get("stats", {}).get("dexterity", 10)`
  - `agents/rules.py:70-90`: `actor.get("name", "Player")`, `actor.get("attacks", [])`
  - `tools/combat.py:120-140`: `target.get("ac", 10)`, `target.get("hp", {}).get("current", 0)`
  - `tools/state_manager.py:40-60`: Saves raw JSON dictionaries without validation.

## Scope

**In scope**:
- `tools/models.py` (Create typed dataclasses: `CharacterModel`, `MonsterModel`, `ItemModel`, `SpellModel`, `LocationModel`, `EncounterModel`, `CheckResultModel`, `AttackResultModel`)
- `tools/state_manager.py` (Add validation helpers: `to_model`, `from_model`)
- `tests/test_domain_models.py` (Unit tests verifying serialization, deserialization, and schema validation)

**Out of scope**:
- Do not break backward-compatibility with dict-based JSON schemas in `state/` and `rules/`.

## Step-by-Step Implementation

### Step 1: Create `tools/models.py`
Define typed `@dataclass` models with `.from_dict()` and `.to_dict()` methods for:
- `CharacterStats(strength, dexterity, constitution, intelligence, wisdom, charisma)`
- `CharacterModel(id, name, species, char_class, level, hp, ac, stats, skills, equipment, spells_prepared)`
- `MonsterModel(id, name, size, monster_type, alignment, ac, hp, speed, stats, skills, cr, xp, traits, actions)`
- `ItemModel(id, name, item_type, rarity, attunement, description, bonuses, charges)`
- `SpellModel(id, name, level, school, casting_time, spell_range, components, duration, description)`

### Step 2: Add validation methods in `tools/models.py`
Provide `validate_character_dict(data: dict) -> Tuple[bool, List[str]]` to ensure required fields are present.

### Step 3: Write tests in `tests/test_domain_models.py`
Verify model instantiation, round-trip serialization to dict, and default fallbacks.

## Verification Gate
Run:
```bash
python -m unittest tests/test_domain_models.py
python dnd.py test
```

## STOP Conditions
- Do not alter existing JSON files under `rules/` or `state/`.
