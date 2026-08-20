# Plan 019: Mechanics Explainability, DC Formulas & Damage Audit Cards

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.

## Status

- **Priority**: P2
- **Effort**: S (1–2 hours)
- **Risk**: LOW
- **Depends on**: 017, 018
- **Category**: ux / explainability
- **Planned at**: commit `v1.0.0-phase4`, 2026-08-20

## Why this matters

In tabletop RPG systems, players and DMs need to understand *why* a check had a specific DC (e.g. Base DC 10 + Dim Lighting +2 + Sentry Alertness +3 = DC 15) and *how* damage was calculated (e.g. 1d8 (6) + STR Mod (+3) + Dragonguard bonus (+1) = 10 piercing damage). Currently, results are presented as opaque single numbers or brief formulas. Providing structured explainability cards for ability checks, attack rolls, damage calculations, and weapon mastery triggers builds complete trust and clarity in the deterministic AI engine.

## Current state

- `tools/mechanics.py:roll_check`: Returns `{"total": 18, "success": True, "formula": "1d20(14)+4"}` without DC factor decomposition.
- `tools/combat.py:roll_damage`: Returns `{"final_damage": 8}` without showing resistance, vulnerability, or weapon mastery triggers.

## Scope

**In scope**:
- `tools/mechanics.py` (Add structured `dc_explanation: List[str]` and `modifier_breakdown: Dict[str, int]` to check and save results)
- `tools/combat.py` (Add `damage_breakdown: List[str]` and `mastery_effect_explanation: Optional[str]` to attack and damage results)
- `tools/formatting.py` (Add visual audit card renderer: `render_mechanics_audit_card()`)
- `tests/test_mechanics_explainability.py` (Unit tests verifying breakdown completeness)

**Out of scope**:
- Do not alter the core mathematical formulas.

## Step-by-Step Implementation

### Step 1: Update `roll_check` and `roll_saving_throw` in `tools/mechanics.py`
Decompose modifiers:
- `ability_mod`: Base stat modifier
- `proficiency_bonus`: If proficient
- `situational_mod`: Guidance, Bardic Inspiration, or cover penalties
- `formula_breakdown`: `d20 ({roll}) + Stat ({mod}) + Prof ({pb}) = {total}`

### Step 2: Update `roll_damage` and `apply_damage` in `tools/combat.py`
Add audit breakdown:
- Dice rolled: `1d8 [6]`
- Stat bonus: `+3 (STR)`
- Magic bonus: `+1 (Dragonguard)`
- Resistances / Immunities applied: `Half damage vs slashing`
- Triggered Weapon Mastery: `Vex (Advantage on next attack against target)`

### Step 3: Add `render_mechanics_audit_card()` in `tools/formatting.py`
Render clean boxed card displaying the full mathematical proof.

### Step 4: Write tests in `tests/test_mechanics_explainability.py`
Verify breakdown calculations and formatting.

## Verification Gate
Run:
```bash
python -m unittest tests/test_mechanics_explainability.py
python dnd.py check stealth 15
python dnd.py attack goblin
python dnd.py test
```

## STOP Conditions
- Ensure backward compatibility of return dictionaries for all existing callers.
