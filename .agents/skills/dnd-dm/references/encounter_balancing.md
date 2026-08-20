# Encounter Balancing Guide (D&D Basic Rules)

Use this guide to balance combat encounters and pace the adventuring day.

---

## 1. Quick CLI Calculation
```bash
# Evaluate encounter difficulty for custom party & monsters
python dnd.py encounter --party "3,3,3,2" --monsters "bugbear:1,hobgoblin:3"

# Evaluate for active party
python dnd.py encounter --monsters "goblin:4,ogre:1"

# With situational modifier (+1 for party drawback, -1 for party benefit)
python dnd.py encounter --monsters "guard:2" --situational 1
```

---

## 2. Difficulty Tiers Explained

- **Easy**: Fast-paced, low-resource encounter. Use for wandering sentries, scouting outposts, or cinematic power demonstrations.
- **Medium**: Standard tactical encounter. Threatens 10-25% of character HP or 1-2 spell slots.
- **Hard**: Significant peril. Spellcaster positioning and tactical mastery are necessary to avoid character knockouts.
- **Deadly**: Boss fights and high-threat climax encounters. Survival requires cooperation, terrain exploitation, and defensive contingency planning.

---

## 3. Pacing the Adventuring Day
- Typical Adventuring Day: **6 to 8 Medium/Hard encounters** between Long Rests.
- Short Rest Cadence: Provide opportunities for short rests after roughly 2 to 3 encounters (~1/3 and 2/3 through the day's XP budget).
