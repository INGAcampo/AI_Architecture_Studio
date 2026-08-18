from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class WorkPackage:
    package_id: str
    domain: str
    dependencies: tuple[str, ...] = ()
    required_gates: tuple[str, ...] = ()
    risk: str = "normal"

@dataclass(frozen=True, slots=True)
class IntegrationPlan:
    waves: tuple[tuple[str, ...], ...]
    package_count: int
    blocked: tuple[str, ...] = ()

class DependencyGraph:
    """Deterministic DAG planner for safe parallel AIAS work packages."""
    def __init__(self, packages: tuple[WorkPackage, ...] = ()) -> None:
        self._packages: dict[str, WorkPackage] = {}
        for package in packages: self.add(package)
    def add(self, package: WorkPackage) -> None:
        if not package.package_id.strip(): raise ValueError("package_id cannot be empty")
        if package.package_id in self._packages: raise ValueError(f"duplicate_package:{package.package_id}")
        self._packages[package.package_id] = package
    def plan(self, completed: set[str] | None = None) -> IntegrationPlan:
        done = set(completed or ())
        unknown = sorted(dep for p in self._packages.values() for dep in p.dependencies if dep not in self._packages and dep not in done)
        if unknown: raise ValueError("unknown_dependencies:" + ",".join(sorted(set(unknown))))
        waves: list[tuple[str, ...]] = []; remaining = set(self._packages) - done
        while remaining:
            ready = tuple(sorted(pid for pid in remaining if set(self._packages[pid].dependencies).issubset(done)))
            if not ready: raise ValueError("dependency_cycle_or_unresolved_gate:" + ",".join(sorted(remaining)))
            waves.append(ready); done.update(ready); remaining.difference_update(ready)
        return IntegrationPlan(tuple(waves), len(self._packages), ())
