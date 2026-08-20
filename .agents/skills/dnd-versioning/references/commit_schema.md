# Commit Record Schema Reference

Every snapshot commit recorded in `state/history.json` adheres to this schema:

```json
{
  "commit_id": "a7f3c91e",
  "parent_id": "c1b9e02a",
  "branch": "main",
  "timestamp": "2026-08-19 20:00:00",
  "intent": "I sneak past Guard Karl, steal the key, and unlock Valen's cell",
  "reason": "Player intent executed via Orchestrator DAG",
  "agent": "Orchestrator",
  "tool_calls": [
    { "tool": "mechanics.check", "skill": "stealth", "dc": 14, "success": true },
    { "tool": "mechanics.check", "skill": "sleight_of_hand", "dc": 14, "success": true }
  ],
  "affected_files": [
    "campaign/npcs/guard_karl.md",
    "campaign/npcs/prisoner_valen.md",
    "state/npcs.json",
    "state/quests.json",
    "state/world.json"
  ],
  "approved_by": null
}
```
