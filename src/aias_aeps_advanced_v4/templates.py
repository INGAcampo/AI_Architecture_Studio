"""Public module supporting advanced AEPS production, governance and observability."""
from __future__ import annotations
from .models import DomainTemplate

def default_templates() -> tuple[DomainTemplate, ...]:
    """Execute the public default_templates operation for advanced AEPS production, governance and observability using explicit caller inputs."""
    return (
        DomainTemplate(
            "TPL-000001",
            "Domain Service",
            "generic",
            {
                "__init__.py": '__version__ = "{{version}}"\n',
                "service.py": (
                    "class {{class_name}}Service:\n"
                    "    \"\"\"Generated domain service for {{domain}}.\"\"\"\n"
                    "    def execute(self, payload):\n"
                    "        return {'domain': '{{domain}}', 'payload': payload, 'status': 'ok'}\n"
                ),
                "contracts.py": (
                    "from typing import Protocol, Any\n\n"
                    "class I{{class_name}}Service(Protocol):\n"
                    "    def execute(self, payload: Any) -> dict: ...\n"
                ),
            },
        ),
        DomainTemplate(
            "TPL-000002",
            "Repository Adapter",
            "generic",
            {
                "repository.py": (
                    "class {{class_name}}Repository:\n"
                    "    def __init__(self):\n"
                    "        self._items = {}\n"
                    "    def save(self, key, value):\n"
                    "        self._items[key] = value\n"
                    "    def get(self, key):\n"
                    "        return self._items[key]\n"
                )
            },
        ),
        DomainTemplate(
            "TPL-000003",
            "Command Handler",
            "generic",
            {
                "commands.py": (
                    "class {{class_name}}CommandHandler:\n"
                    "    def handle(self, command):\n"
                    "        return {'command': command, 'handled': True}\n"
                )
            },
        ),
    )
