"""Public module supporting advanced AEPS production, governance and observability."""
from __future__ import annotations
from pathlib import Path

class ContractGenerator:
    """Execute the public ContractGenerator operation for advanced AEPS production, governance and observability using explicit caller inputs."""
    def generate(self, module_name: str, class_name: str, output: Path) -> Path:
        """Build the generate required by advanced AEPS production, governance and observability from explicit inputs."""
        package = output / "src" / module_name
        package.mkdir(parents=True, exist_ok=True)
        path = package / "api.py"
        path.write_text(
            "from typing import Protocol, Any\n\n"
            f"class I{class_name}(Protocol):\n"
            "    def execute(self, payload: Any) -> dict: ...\n",
            encoding="utf-8",
        )
        return path
