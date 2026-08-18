"""Public module supporting advanced AEPS production, governance and observability."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Any

@dataclass(slots=True)
class Migration:
    """Execute the public Migration operation for advanced AEPS production, governance and observability using explicit caller inputs."""
    migration_id: str
    from_version: str
    to_version: str
    apply_fn: Callable[[dict], dict]
    rollback_fn: Callable[[dict], dict]

@dataclass(slots=True)
class MigrationEngine:
    """Execute the public MigrationEngine operation for advanced AEPS production, governance and observability using explicit caller inputs."""
    migrations: list[Migration] = field(default_factory=list)

    def register(self, migration: Migration) -> None:
        """Add register to advanced AEPS production, governance and observability while enforcing identity constraints."""
        self.migrations.append(migration)

    def migrate(self, payload: dict, from_version: str, to_version: str) -> dict:
        """Execute the public MigrationEngine.migrate operation for advanced AEPS production, governance and observability using explicit caller inputs."""
        current = dict(payload)
        version = from_version
        for migration in self.migrations:
            if migration.from_version == version:
                current = migration.apply_fn(current)
                version = migration.to_version
                if version == to_version:
                    return current
        if version != to_version:
            raise ValueError(f"No migration path from {from_version} to {to_version}")
        return current

    def rollback(self, payload: dict, from_version: str, to_version: str) -> dict:
        """Execute the public MigrationEngine.rollback operation for advanced AEPS production, governance and observability using explicit caller inputs."""
        current = dict(payload)
        version = from_version
        for migration in reversed(self.migrations):
            if migration.to_version == version:
                current = migration.rollback_fn(current)
                version = migration.from_version
                if version == to_version:
                    return current
        if version != to_version:
            raise ValueError(f"No rollback path from {from_version} to {to_version}")
        return current
