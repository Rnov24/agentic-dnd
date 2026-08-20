# Security Policy

## 🔒 Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

---

## 🛡️ Sandbox & Security Model

Agentic D&D operates under a **Dual Mode Security Sandbox**:

1. **Game Mode (Default)**:
   - AI Agents operate strictly within allowlisted campaign boundaries (`campaign/`, `state/`).
   - Read/write access is restricted to verified tool interfaces decorated with `@dnd_tool`.
   - Execution of arbitrary shell commands or code evaluation is strictly forbidden.
   - **Consequential Change Gate**: High-impact irreversible actions (character death, major NPC death, quest failure) require human confirmation prior to persistence.

2. **Developer Mode**:
   - Elevated developer authority to inspect schemas, build tools, and run test suites.
   - Protected by `@developer_only` security barriers in `tools/permissions.py`.

---

## 🚨 Reporting a Vulnerability

If you discover a security issue or vulnerability within Agentic D&D, please **do not open a public GitHub issue**.

Instead, please report vulnerabilities by emailing the core maintainers or using GitHub Private Vulnerability Reporting.

Please include:
- Description of the issue and potential impact
- Steps to reproduce
- Proposed remediation or patch (if available)

We will respond promptly within 48 hours and work with you on a coordinated disclosure.
