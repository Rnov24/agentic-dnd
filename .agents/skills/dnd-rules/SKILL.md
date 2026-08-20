---
name: dnd-rules
description: D&D 5e (2024 revision) mechanics arbiter, ability checks, weapon mastery properties, spellcasting rules, saving throws, DCs, attack resolution, and condition effects for Agentic D&D. Use whenever evaluating rules legality, determining DCs, calculating modifiers, rolling dice, validating actions, or looking up conditions and masteries, even if the user asks simple questions like 'what is my stealth modifier?' or 'does topple work on this hit?'.
---

# D&D 5e (2024 Revision) Rules Engine Skill

This skill provides the definitive mechanical guidelines and deterministic tool execution patterns for the **2024 revision of D&D 5th Edition**.

---

## Why Python Determinism is Required
All ability checks, attack rolls, damage calculations, and saving throws must execute through Python tools ([`tools/mechanics.py`](file:///d:/Projects/agentic-dnd/tools/mechanics.py), [`tools/combat.py`](file:///d:/Projects/agentic-dnd/tools/combat.py), [`tools/dice.py`](file:///d:/Projects/agentic-dnd/tools/dice.py)) or the CLI (`dnd.py`). This guarantees zero arithmetic hallucinations and maintains state integrity.

---

## Quick CLI Mechanics Commands

### 1. Tabletop Dice Rolling
```bash
# Standard roll with bonus
python dnd.py roll "1d20+5"

# Advantage / Disadvantage (rolls 2d20, takes higher/lower)
python dnd.py roll "1d20+7" --adv
python dnd.py roll "1d20+3" --disadv

# Critical Hit (automatically doubles weapon damage dice)
python dnd.py roll "2d6+3" --crit
```

### 2. Ability & Skill Checks (D20 Tests)
```bash
# Stealth check vs DC 15
python dnd.py check stealth 15

# Sleight of Hand check with Advantage and Guidance (+1d4)
python dnd.py check sleight_of_hand 14 --adv --guidance

# Specific character check
python dnd.py check arcana 16 --character eldrin_shadowseeker
```

### 3. Combat Attacks vs AC
```bash
# Attack target with equipped weapon
python dnd.py attack guard_karl --weapon "Black Glass Dagger"

# Attack with advantage from hidden/stealth position
python dnd.py attack guard_karl --weapon "Black Glass Dagger" --adv
```

---

## D&D 2024 Core Rules Reference

### 1. The D20 Test
$$\text{Total} = \text{d20 Roll} + \text{Ability Modifier} + \text{Proficiency (if applicable)} + \text{Circumstantial Modifiers}$$
- **Natural 20**: Automatic hit in combat. Grants **Heroic Inspiration** in 2024 rules.
- **Natural 1**: Automatic miss in combat.

### 2. Standard Difficulty Classes (DC)
- **Very Easy (DC 5)**: Noticeable environmental details, climbing an untied ladder.
- **Easy (DC 10)**: Recalling common regional lore, hearing un-muffled voices.
- **Medium (DC 15)**: Picking a standard prison cell lock, sneaking past an alert sentry.
- **Hard (DC 20)**: Picking a masterwork vault, recalling forgotten arcane rites.
- **Very Hard (DC 25)**: Countering high-circle abjuration wards.
- **Nearly Impossible (DC 30)**: Tracking an invisible assassin across wet flagstones during a storm.

### 3. 2024 Weapon Mastery System (8 Masteries)
- **Cleave**: On melee hit, make a second attack vs an adjacent enemy within 5ft.
- **Graze**: On miss, target still takes damage equal to your ability modifier.
- **Nick**: Make an off-hand Light weapon attack as part of the Attack action instead of a Bonus Action.
- **Push**: On hit, push target up to 10ft away if Large or smaller.
- **Sap**: On hit, target has Disadvantage on its next attack before your next turn.
- **Slow**: On hit and damage, reduce target speed by 10ft until your next turn.
- **Topple**: On hit, target makes a CON save (DC = 8 + Str Mod + Prof) or falls Prone.
- **Vex**: On hit and damage, gain Advantage on your next attack against that target.

---

## Bundled References
- Complete 2024 Weapon Masteries: [`references/weapon_masteries.md`](references/weapon_masteries.md)
- Complete 14 Conditions Guide: [`references/conditions_guide.md`](references/conditions_guide.md)
- DC Benchmarks for All Abilities: [`references/dc_benchmarks.md`](references/dc_benchmarks.md)
