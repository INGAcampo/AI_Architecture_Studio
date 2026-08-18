"""Directed typed ontology relationships for engineering concepts."""
from __future__ import annotations
from dataclasses import dataclass, field

@dataclass(slots=True)
class OntologyGraph:
    """Store concept nodes and query typed incoming and outgoing relationships."""
    triples: set[tuple[str, str, str]] = field(default_factory=set)

    def add(self, subject: str, predicate: str, obj: str) -> None:
        """Add an idempotent directed subject-predicate-object relationship."""
        self.triples.add((subject, predicate, obj))

    def objects(self, subject: str, predicate: str | None = None) -> tuple[str, ...]:
        """Return sorted objects related from a subject, optionally by predicate."""
        return tuple(sorted({
            obj for s, p, obj in self.triples
            if s == subject and (predicate is None or p == predicate)
        }))

    def subjects(self, predicate: str, obj: str) -> tuple[str, ...]:
        """Return sorted subjects pointing to an object through a predicate."""
        return tuple(sorted({s for s, p, o in self.triples if p == predicate and o == obj}))

    def related(self, node: str) -> tuple[str, ...]:
        """Return all directly incoming or outgoing neighbors of a concept."""
        result = set()
        for s, _, o in self.triples:
            if s == node: result.add(o)
            if o == node: result.add(s)
        return tuple(sorted(result))
