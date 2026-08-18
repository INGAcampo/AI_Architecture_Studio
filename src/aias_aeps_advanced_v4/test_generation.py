"""Public module supporting advanced AEPS production, governance and observability."""
from __future__ import annotations
from pathlib import Path

class AdvancedTestGenerator:
    """Execute the public AdvancedTestGenerator operation for advanced AEPS production, governance and observability using explicit caller inputs."""
    def generate(self, module_name: str, class_name: str, output: Path) -> list[Path]:
        """Build the generate required by advanced AEPS production, governance and observability from explicit inputs."""
        tests = output / "tests"
        tests.mkdir(parents=True, exist_ok=True)
        unit = tests / f"test_{module_name}_unit.py"
        unit.write_text(
            f"from {module_name}.service import {class_name}Service\n\n"
            "def test_execute_contract():\n"
            f"    result = {class_name}Service().execute({{'x': 1}})\n"
            "    assert result['status'] == 'ok'\n",
            encoding="utf-8",
        )
        integration = tests / f"test_{module_name}_integration.py"
        integration.write_text(
            f"from {module_name}.service import {class_name}Service\n\n"
            "def test_generated_integration_flow():\n"
            f"    service = {class_name}Service()\n"
            "    result = service.execute({'integration': True})\n"
            "    assert result['payload']['integration'] is True\n",
            encoding="utf-8",
        )
        return [unit, integration]
