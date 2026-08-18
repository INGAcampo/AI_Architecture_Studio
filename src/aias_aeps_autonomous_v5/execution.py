"""Public module supporting autonomous engineering planning and controlled execution."""
from __future__ import annotations
from pathlib import Path
import os, subprocess, sys

class WorkspaceTestRunner:
    """Execute the public WorkspaceTestRunner operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
    def run(self, workspace: Path) -> dict:
        """Execute run for autonomous engineering planning and controlled execution with validated state transitions."""
        env = dict(os.environ)
        env["PYTHONPATH"] = str(workspace / "src") + os.pathsep + env.get("PYTHONPATH", "")
        env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(workspace / "tests"), "-q"],
            cwd=workspace,
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
        )
        return {
            "passed": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
