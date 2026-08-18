"""Public module supporting autonomous engineering planning and controlled execution."""
from __future__ import annotations
from pathlib import Path

class SecurityPolicyEngine:
    """Execute the public SecurityPolicyEngine operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
    FORBIDDEN_NAMES = {".env", "secrets.json", "credentials.json"}

    def scan_specification(self, specification: dict) -> list[str]:
        """Execute the public SecurityPolicyEngine.scan_specification operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
        issues = []
        text = str(specification).lower()
        for token in ("password", "private_key", "api_key"):
            if token in text:
                issues.append(f"forbidden_secret_field:{token}")
        return issues

    def scan_workspace(self, workspace: Path) -> list[str]:
        """Execute the public SecurityPolicyEngine.scan_workspace operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
        issues = []
        for path in workspace.rglob("*"):
            if path.is_file() and path.name.lower() in self.FORBIDDEN_NAMES:
                issues.append(f"forbidden_file:{path.name}")
        return issues
