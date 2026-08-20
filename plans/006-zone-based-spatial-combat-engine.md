# Plan 006: Design & Spike — Theater of the Mind Zone-Based Spatial Combat Engine

> **Executor instructions**: This is a Design & Spike Plan for forward-looking
> product direction. Build the specified prototype module, run its verification
> tests, and record open design questions in `plans/README.md`.

## Status

- **Priority**: P3
- **Effort**: M (1–2 days)
- **Risk**: LOW
- **Depends on**: none
- **Category**: direction
- **Planned at**: 2026-08-20

## Why this matters

Tabletop D&D 5e relies on movement, spell ranges (e.g. 5ft, 30ft, 60ft, 120ft), and opportunity attacks. In AI-native Theater of the Mind, asking players for 5-foot grid coordinates (`x,y`) slows gameplay, while ignoring distance completely trivializes ranged weapons and movement abilities. Implementing a 3-tier **Zone Combat Model** (*Engaged / Close / Near / Far*) provides rich tactical positioning, deterministic range checking, and movement action costs while keeping narration seamless.

## Current state

- `tools/combat.py`: Resolves `roll_attack`, `roll_damage`, and `apply_damage` but tracks no spatial positioning.
- `tools/cover.py`: Resolves Half Cover (+2 AC), Three-Quarters (+5 AC), and Total Cover.
- `state/combat.json`: Contains combatants and turn order, but no location zones.

## Scope

**In scope**:
- `tools/zones.py` (Create new module managing spatial zones: `Zone`, `SpatialCombatManager`, `distance_between`, `can_attack_with_weapon`, `move_combatant`)
- `tests/test_zones.py` (Unit tests for zone transitions and weapon range validation)
- `dnd.py` (Add optional `--zone` and `dnd.py zone [show/move]` CLI commands)

**Out of scope**:
- Do not require rigid 2D grid coordinates.
- Do not break existing non-zoned `dnd.py attack` commands (default zone = `Engaged`).

## Step-by-Step Implementation

### Step 1: Define Zone Enum and Data Structures in `tools/zones.py`
```python
from enum import Enum

class TacticalZone(str, Enum):
    ENGAGED = "engaged"   # Melee range (within 5 ft)
    CLOSE = "close"       # Short range (within 15 ft)
    NEAR = "near"         # Standard range (15–30 ft)
    FAR = "far"           # Long range (30–60 ft+)
```

### Step 2: Implement `SpatialCombatManager`
1. `assign_zone(combatant_id: str, zone: TacticalZone)`
2. `get_zone(combatant_id: str) -> TacticalZone`
3. `can_attack_target(attacker_id: str, target_id: str, weapon: Dict[str, Any]) -> Tuple[bool, str]`
4. `move_combatant(combatant_id: str, target_zone: TacticalZone, has_dash: bool = False) -> Dict[str, Any]`

### Step 3: Write Unit Tests in `tests/test_zones.py`
- Test melee attacks are permitted only in `ENGAGED` or `CLOSE`.
- Test ranged weapons (Longbow, Shortbow, Fire Bolt) can target `NEAR` and `FAR`.
- Test opportunity attack triggers when disengaging from `ENGAGED` without Disengage action.

## Verification Gate
Run:
```bash
python -m unittest tests/test_zones.py
python dnd.py test
```

## STOP Conditions
- If zone rules conflict with `tools/combat.py`, ensure spatial checks are strictly additive and default gracefully when zones are unassigned.
