---
name: dnd-spells
description: D&D 5e (2024 revision) magic, spellcasting engine, slot management, concentration arbitration, ritual casting, upcasting, and counterspell resolution for Agentic D&D. Use whenever a character casts a spell, prepares spells, manages spell slots, makes concentration saves, or resolves magical effects, even if the user says 'I cast Fire Bolt' or 'check Eldrin spell slots'.
---

# Spellcasting & Magic Engine Skill (5e 2024 Revision)

This skill governs spellcasting rules, spell slot consumption, concentration tracking, upcasting calculations, and ritual casting under the 2024 revision of D&D 5e.

---

## Core 2024 Magic Rules

### 1. Spell Slots & Cantrips
- **Cantrips**: Cast without consuming spell slots. Damage scales automatically at character levels 1, 5, 11, and 17 (e.g. *Fire Bolt* deals 1d10 at lvl 1-4, 2d10 at lvl 5-10).
- **Leveled Spells (1st-9th)**: Consumes one spell slot of the chosen level from `state/party.json`.

### 2. Concentration Tracking & DC Calculation
- A caster can concentrate on only **one** spell at a time.
- When taking damage while concentrating, the caster must succeed on a Constitution saving throw:
  $$\text{Concentration DC} = \max\left(10, \left\lfloor \frac{\text{Damage Taken}}{2} \right\rfloor\right)$$
- If the save fails, the spell effect terminates immediately and concentration is cleared.

### 3. Ritual Casting (2024 Revision)
Any character with a prepared spell tagged as a Ritual can cast it as a ritual by adding 10 minutes to the normal casting time. Ritual casting consumes **0 spell slots**.

### 4. Counterspell Resolution (2024 Revision)
In the 2024 rules, *Counterspell* forces the targeted caster to make a **Constitution saving throw** against the counterspeller's Spell Save DC. On a failure, the spell fails and the slot is wasted.

---

## Quick Spell Commands

```bash
# Process spellcasting through orchestrator
python dnd.py play "Eldrin casts Fire Bolt at Guard Karl"

# Cast a leveled spell with spell slot deduction
python dnd.py play "Eldrin casts Mage Armor on himself"
```

---

## Concrete Magic Examples

### Example 1: Cantrip Attack
- **Player Input**: `"Eldrin hurls a mote of fire at the approaching guard."`
- **Resolution**: Rules Agent executes ranged spell attack (d20 + INT Mod + Prof vs AC). On hit, deals 1d10 fire damage. Consumes 0 spell slots.

### Example 2: Concentration Save Under Fire
- **Scenario**: Eldrin is concentrating on *Detect Magic* and takes 14 slashing damage.
- **Resolution**: Triggers Concentration Constitution saving throw vs DC 10 (since $\lfloor 14/2 \rfloor = 7 < 10$). Python rolls d20 + CON Mod. If failed, *Detect Magic* ends.

---

## Bundled References
- Detailed Spellcasting Rules & Upcasting: [`references/spellcasting_rules.md`](references/spellcasting_rules.md)
- Spell Compendium Cheat Sheet: [`references/spells_compendium.md`](references/spells_compendium.md)
