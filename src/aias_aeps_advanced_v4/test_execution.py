"""Public module supporting advanced AEPS production, governance and observability."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import os, subprocess, sys

@dataclass(frozen=True, slots=True)
class TestExecutionResult:
    """Execute the public TestExecutionResult operation for advanced AEPS production, governance and observability using explicit caller inputs."""
    returncode: int
    stdout: str
    stderr: str
    passed: bool

class GeneratedTestExecutor:
    """Execute the public GeneratedTestExecutor operation for advanced AEPS production, governance and observability using explicit caller inputs."""
    def run(self, workspace: Path) -> TestExecutionResult:
        """Execute run for advanced AEPS production, governance and observability with validated state transitions."""
        env = dict(os.environ)
        src = workspace / "src"
        env["PYTHONPATH"] = str(src) + os.pathsep + env.get("PYTHONPATH", "")
        env["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(workspace / "tests"), "-q"],
            cwd=workspace,
            env=env,
            capture_output=True,
            text=True,
            timeout=60,
        )
        return TestExecutionResult(
            result.returncode,
            result.stdout,
            result.stderr,
            result.returncode == 0,
        )
