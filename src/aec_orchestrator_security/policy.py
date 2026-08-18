from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class OperationPolicy:
    application: str
    allowed_operations: tuple[str,...]
    destructive_operations: tuple[str,...] = ()
    publish_operations: tuple[str,...] = ()

    def validate(self) -> None:
        if not self.application.strip():
            raise ValueError("application must not be empty")
        if set(self.destructive_operations)-set(self.allowed_operations):
            raise ValueError("destructive operations must be declared allowed")
        if set(self.publish_operations)-set(self.allowed_operations):
            raise ValueError("publish operations must be declared allowed")
