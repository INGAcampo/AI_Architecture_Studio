"""Public module supporting the Omega application core and shared runtime services."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

@dataclass(frozen=True, slots=True)
class CommandResult:
    """Execute the public CommandResult operation for the Omega application core and shared runtime services using explicit caller inputs."""
    ok: bool
    value: Any = None
    message: str = ""

class CommandBus:
    """Execute the public CommandBus operation for the Omega application core and shared runtime services using explicit caller inputs."""
    def __init__(self) -> None:
        self._commands: dict[str, Callable[..., Any]] = {}
        self.history: list[str] = []

    def register(self, name: str, callback: Callable[..., Any]) -> None:
        """Add register to the Omega application core and shared runtime services while enforcing identity constraints."""
        key = name.strip().lower()
        if key in self._commands:
            raise ValueError(f"Command already registered: {name}")
        self._commands[key] = callback

    def execute(self, name: str, *args, **kwargs) -> CommandResult:
        """Execute execute for the Omega application core and shared runtime services with validated state transitions."""
        key = name.strip().lower()
        if key not in self._commands:
            return CommandResult(False, message=f"Unknown command: {name}")
        self.history.append(key)
        try:
            return CommandResult(True, self._commands[key](*args, **kwargs))
        except Exception as exc:
            return CommandResult(False, message=str(exc))
