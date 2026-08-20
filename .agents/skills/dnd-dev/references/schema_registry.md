# Structured Schema Registry Guidelines

All state files in `state/` must comply with strict JSON schemas:

1. **Party Schema (`state/party.json`)**:
   - `id` (string), `name` (string), `class` (string), `level` (int 1-20), `ac` (int >= 1)
   - `hp`: `{ "current": int >= 0, "max": int >= 1, "temp": int >= 0 }`
   - `stats`: `{ "strength": int, "dexterity": int, "constitution": int, "intelligence": int, "wisdom": int, "charisma": int }`
   - `conditions`: list of strings matching `rules/dnd2024/conditions.md`

2. **NPC Schema (`state/npcs.json`)**:
   - `id` (string), `name` (string), `role` (string), `status` ("Alive"|"Dead"|"Unconscious")
   - `disposition`: int (-100 to +100)
   - `memory_stream`: list of `{ "turn": int, "event": str, "disposition_delta": int }`

3. **World Schema (`state/world.json`)**:
   - `active_location` (string), `time_of_day` (string), `weather` (string), `lighting` (string)
   - `tension_level` ("Calm"|"Tense"|"High"|"Combat")
   - `current_scene`: `{ "title": str, "description": str, "threats": list, "exits": list }`
