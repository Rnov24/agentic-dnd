# D&D 5e (2024 Revision) Core Mechanics

## The Core Rule: The d20 Test

Whenever a creature attempts an action that has a chance of meaningful failure, the Dungeon Master calls for a **d20 Test**.

A d20 Test follows this formula:

$$\text{Total} = \text{d20 Roll} + \text{Ability Modifier} + \text{Proficiency Bonus (if proficient)} + \text{Situational Bonuses}$$

If $\text{Total} \ge \text{Target DC or AC}$, the test succeeds.

## Types of d20 Tests
1. **Ability Checks**: Testing a creature's innate talent and training against an environmental or social challenge.
2. **Attack Rolls**: Testing combat prowess against a target's Armor Class (AC).
3. **Saving Throws**: Resisting an incoming hazard, spell, poison, or psychological trauma.

## Advantage and Disadvantage
- **Advantage**: Roll two d20s and use the higher result.
- **Disadvantage**: Roll two d20s and use the lower result.
- If multiple sources grant Advantage and Disadvantage, they cancel out into a standard single roll.

## Critical Hits and Fumbles
- **Natural 20**: Automatic hit on attack rolls; roll all damage dice twice. Automatic success on death saves (regain 1 HP).
- **Natural 1**: Automatic miss on attack rolls. Counts as two failures on death saving throws.

## Deterministic Execution
All d20 tests in Agentic D&D are computed through the Python deterministic runtime (`tools/dice.py` and `tools/mechanics.py`). The LLM never hallucinates dice results.
