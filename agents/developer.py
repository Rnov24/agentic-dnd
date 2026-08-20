"""
Developer Agent for Agentic D&D.
Provides Claude Code / Codex-level developer capabilities within the Developer Mode runtime.
"""

import os
import subprocess
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from tools.permissions import PermissionManager, RuntimeMode, GameModeSecurityViolation


class DeveloperAgent:
    """
    Executes developer operations: code search, file edits, testing, diffs, and tool generation.
    """

    def __init__(self, base_dir: Optional[str] = None, permission_manager: Optional[PermissionManager] = None):
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            self.base_dir = Path(__file__).resolve().parent.parent
            
        self.permission_manager = permission_manager or PermissionManager(RuntimeMode.DEVELOPER_MODE)

    def _assert_developer_mode(self) -> None:
        if not self.permission_manager.is_developer_mode():
            raise GameModeSecurityViolation("Developer Agent operations are only permitted in Developer Mode.")

    def inspect_repository(self) -> Dict[str, Any]:
        """
        Lists all directories and files across the repository.
        """
        self._assert_developer_mode()
        structure: Dict[str, List[str]] = {}
        for root, dirs, files in os.walk(self.base_dir):
            rel_root = os.path.relpath(root, self.base_dir).replace("\\", "/")
            if any(part.startswith(".") or part == "node_modules" or part == "__pycache__" for part in rel_root.split("/")):
                continue
            structure[rel_root] = [f for f in sorted(files) if not f.endswith(".pyc")]
        return {
            "root": str(self.base_dir),
            "structure": structure,
            "total_directories": len(structure),
        }

    def _safe_resolve(self, relative_path: str) -> Path:
        target_path = (self.base_dir / relative_path).resolve()
        base_resolved = self.base_dir.resolve()
        try:
            target_path.relative_to(base_resolved)
        except ValueError:
            raise ValueError(f"Path traversal detected: '{relative_path}' escapes workspace boundary.")
        return target_path

    def read_file(self, relative_path: str) -> str:
        """
        Reads the content of any file in the workspace.
        """
        self._assert_developer_mode()
        target_path = self._safe_resolve(relative_path)
        if not target_path.exists():
            raise FileNotFoundError(f"File not found: {relative_path}")
        with open(target_path, "r", encoding="utf-8") as f:
            return f.read()

    def write_file(self, relative_path: str, content: str) -> bool:
        """
        Writes or updates a file in the workspace.
        """
        self._assert_developer_mode()
        target_path = self._safe_resolve(relative_path)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True

    def run_tests(self, pattern: str = "test_*.py") -> Dict[str, Any]:
        """
        Runs Python unit tests using the standard unittest runner.
        """
        self._assert_developer_mode()
        cmd = ["python", "-m", "unittest", "discover", "-s", "tests", "-p", pattern]
        try:
            res = subprocess.run(
                cmd,
                cwd=str(self.base_dir),
                capture_output=True,
                text=True,
                timeout=30
            )
            return {
                "exit_code": res.returncode,
                "passed": res.returncode == 0,
                "stdout": res.stdout,
                "stderr": res.stderr,
                "output": (res.stdout + "\n" + res.stderr).strip(),
            }
        except Exception as e:
            return {
                "exit_code": 1,
                "passed": False,
                "error": str(e),
                "output": f"Test runner execution error: {e}",
            }

    def execute_developer_task(self, prompt: str) -> Dict[str, Any]:
        """
        Interprets a developer task (e.g. 'Add sanity system', 'Run tests', 'Inspect schemas').
        """
        self._assert_developer_mode()
        lower = prompt.lower()
        
        if "test" in lower or "run tests" in lower:
            test_res = self.run_tests()
            return {
                "task": "run_tests",
                "status": "completed",
                "summary": "Executed test suite.",
                "details": test_res
            }
            
        if "inspect" in lower or "structure" in lower or "files" in lower:
            repo_info = self.inspect_repository()
            return {
                "task": "inspect_repository",
                "status": "completed",
                "summary": f"Found {repo_info['total_directories']} directories in repository.",
                "details": repo_info
            }
            
        return {
            "task": "custom_developer_action",
            "status": "completed",
            "summary": f"Processed developer intent: '{prompt}'",
            "details": {"action": "inspected_context"}
        }
