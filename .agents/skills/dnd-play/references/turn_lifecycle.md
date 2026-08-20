# Multi-Agent Turn Lifecycle Reference

This document details the responsibilities and interaction boundaries of each agent during a turn.

```text
Player Intent
      │
      ▼
[Orchestrator] ──► Inspects party.json, world.json, active location
      │
      ├─► [World Agent]: Checks environmental conditions (Dim Light -> Stealth Advantage)
      ├─► [Rules Agent]: Determines required D20 Test (Skill, DC, Ability)
      ├─► [Python Mechanics]: Calculates d20 roll, modifiers, crits, and final margin
      ├─► [Combat Agent]: Resolves damage, resistances, and temp HP absorption
      ├─► [NPC Cognitive Agent]: Modifies NPC disposition score (-100 to +100) and memory stream
      ├─► [Character Agent]: Coordinates AI companion assist actions and tactical banter
      ├─► [State Agent]: Applies schema-validated mutations to state/*.json and campaign/*.md
      ├─► [Impact Agent]: Assesses change tier (Low/Medium/High/Critical)
      ├─► [Chronos Agent]: Generates SHA-256 snapshot commit and stores state diff
      └─► [DM Agent]: Synthesizes all data into atmospheric Theater-of-the-Mind prose
```
