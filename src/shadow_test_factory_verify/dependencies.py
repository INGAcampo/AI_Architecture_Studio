from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DependencyValidation:
    passed: bool
    violations: tuple[str,...]


def validate_dependency_order(entries) -> DependencyValidation:
    names=[str(item["megablock"]) for item in entries]
    position={name:index for index,name in enumerate(names)}
    violations=[]

    for item in entries:
        name=str(item["megablock"])
        dependency=str(item.get("dependency",""))

        if not dependency:
            continue

        if dependency not in position:
            violations.append(f"{name}: missing dependency {dependency}")
            continue

        if position[dependency]>=position[name]:
            violations.append(f"{name}: dependency order violation for {dependency}")

    return DependencyValidation(
        passed=not violations,
        violations=tuple(violations),
    )
