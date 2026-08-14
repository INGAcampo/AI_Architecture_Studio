from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class DependencyClosureAudit:
    passed:bool
    missing_dependencies:tuple[str,...]
    self_dependencies:tuple[str,...]

def audit_dependency_closure(entries)->DependencyClosureAudit:
    values=tuple(entries)
    names={str(item.get("megablock","")) for item in values}
    missing=[]
    selfdeps=[]

    for item in values:
        name=str(item.get("megablock",""))
        dep=str(item.get("dependency",""))

        if not dep:
            continue

        if dep==name:
            selfdeps.append(name)
            continue

        if dep not in names:
            missing.append(name+"->"+dep)

    return DependencyClosureAudit(
        passed=not missing and not selfdeps,
        missing_dependencies=tuple(sorted(missing)),
        self_dependencies=tuple(sorted(selfdeps)),
    )
