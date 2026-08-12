from __future__ import annotations

import ast
import importlib.util
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = PROJECT_ROOT / "scripts" / "test.py"


def load_runner_module():
    spec = importlib.util.spec_from_file_location("aias_test_runner", RUNNER_PATH)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_runner_is_valid_python() -> None:
    source = RUNNER_PATH.read_text(encoding="utf-8-sig")
    ast.parse(source, filename=str(RUNNER_PATH))


def test_runner_builds_expected_pytest_command() -> None:
    module = load_runner_module()

    class Args:
        collect_only = False
        fast = True
        path = "tests/test_s0_02_repository_tools.py"
        pytest_args = []

    command = module.build_command(Args())

    assert command[:3] == [module.sys.executable, "-m", "pytest"]
    assert "-q" in command
    assert "--maxfail=1" in command
    assert command[-1] == "tests/test_s0_02_repository_tools.py"
