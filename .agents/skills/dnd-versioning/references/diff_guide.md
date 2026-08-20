# Unified Diff Guide for Agentic D&D

Unified diffs represent changes across both JSON state and Markdown files:

```diff
--- state/npcs.json (Commit: c1b9e02a)
+++ state/npcs.json (Commit: a7f3c91e)
@@ -12,4 +12,4 @@
-  "status": "Imprisoned",
+  "status": "Freed",
-  "disposition": "Frightened",
+  "disposition": "Grateful (+40)"

--- campaign/npcs/prisoner_valen.md (Commit: c1b9e02a)
+++ campaign/npcs/prisoner_valen.md (Commit: a7f3c91e)
@@ -20,3 +20,3 @@
-## Current Status: Imprisoned in Cell #3
+## Current Status: Escaping with Aria Nightwind
```
