"""Bidirectional requirement relationship, coverage and impact analysis."""
from dataclasses import dataclass, field

@dataclass(slots=True)
class TraceabilityMatrix:
    """Store typed links and measure implementation-plus-test requirement coverage."""
    links: dict[str, dict[str, set[str]]] = field(default_factory=dict)

    def link(self, source_id: str, relation: str, target_id: str) -> None:
        """Add an idempotent typed relationship between stable asset identities."""
        self.links.setdefault(source_id, {}).setdefault(relation, set()).add(target_id)

    def targets(self, source_id: str, relation: str) -> tuple[str, ...]:
        """Return sorted targets for a source and relationship type."""
        return tuple(sorted(self.links.get(source_id, {}).get(relation, set())))

    def coverage(self, requirement_ids: list[str]) -> float:
        """Measure requirements linked to both implementation and automated tests."""
        if not requirement_ids:
            return 1.0
        complete = 0
        for req_id in requirement_ids:
            rels = self.links.get(req_id, {})
            if rels.get("implemented_by") and rels.get("tested_by"):
                complete += 1
        return complete / len(requirement_ids)

    def impact(self, changed_id: str) -> set[str]:
        """Return directly connected sources and targets affected by an identity change."""
        affected = set()
        for src, relations in self.links.items():
            for targets in relations.values():
                if changed_id in targets:
                    affected.add(src)
            if src == changed_id:
                for targets in relations.values():
                    affected.update(targets)
        return affected
