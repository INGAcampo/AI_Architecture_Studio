"""Public module supporting autonomous engineering planning and controlled execution."""
from __future__ import annotations
from pathlib import Path
import json, re

def safe_name(value: str) -> str:
    """Execute the public safe_name operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
    name = re.sub(r"[^a-zA-Z0-9_]+", "_", value).strip("_").lower()
    return name or "generated_module"

class MultiDomainProgramGenerator:
    """Execute the public MultiDomainProgramGenerator operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
    def generate(self, specification: dict, workspace: Path) -> list[Path]:
        """Build the generate required by autonomous engineering planning and controlled execution from explicit inputs."""
        module = safe_name(specification["module_name"])
        package = workspace / "src" / module
        tests = workspace / "tests"
        docs = workspace / "docs"
        package.mkdir(parents=True, exist_ok=True)
        tests.mkdir(parents=True, exist_ok=True)
        docs.mkdir(parents=True, exist_ok=True)

        init = package / "__init__.py"
        init.write_text(f'__version__ = "{specification["version"]}"\n', encoding="utf-8")

        domain = package / "domain.py"
        domain.write_text(
            "class GeneratedProgram:\n"
            f"    domain = {specification.get('domain', 'generic')!r}\n"
            "    def capabilities(self):\n"
            f"        return {specification.get('capabilities', [])!r}\n",
            encoding="utf-8",
        )

        test = tests / f"test_{module}.py"
        test.write_text(
            f"from {module}.domain import GeneratedProgram\n\n"
            "def test_generated_program():\n"
            "    assert isinstance(GeneratedProgram().capabilities(), list)\n",
            encoding="utf-8",
        )

        readme = docs / "README.md"
        readme.write_text(
            f"# {specification['title']}\n\n"
            f"Domain: {specification.get('domain','generic')}\n",
            encoding="utf-8",
        )

        trace = docs / "traceability.json"
        trace.write_text(json.dumps({
            "specification_id": specification["id"],
            "requirements": specification.get("requirements", []),
            "capabilities": specification.get("capabilities", []),
        }, indent=2), encoding="utf-8")
        return [init, domain, test, readme, trace]
