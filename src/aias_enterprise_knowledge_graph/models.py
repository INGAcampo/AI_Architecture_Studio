"""Immutable node and edge contracts for the AIAS enterprise knowledge graph."""
from __future__ import annotations
from dataclasses import asdict, dataclass, field


@dataclass(frozen=True, slots=True)
class Node:
    """Represent a versioned enterprise concept with attributable evidence."""
    node_id: str
    node_type: str
    name: str
    version: str = "1.0.0"
    properties: dict = field(default_factory=dict)
    provenance: dict = field(default_factory=dict)

    def validate(self) -> None:
        """Reject incomplete or unattributed enterprise concepts."""
        if not self.node_id or not self.node_type or not self.name:
            raise ValueError("invalid_node")
        if not self.provenance.get("source"):
            raise ValueError("missing_provenance")

    def to_dict(self) -> dict:
        """Serialize the node into its canonical persistent representation."""
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Edge:
    """Represent a typed, temporal and attributable directed relationship."""
    edge_id: str
    source: str
    relation: str
    target: str
    version: str = "1.0.0"
    valid_from: str | None = None
    valid_to: str | None = None
    properties: dict = field(default_factory=dict)
    provenance: dict = field(default_factory=dict)

    def validate(self) -> None:
        """Reject incomplete, self-referential or unattributed relationships."""
        if not all((self.edge_id, self.source, self.relation, self.target)):
            raise ValueError("invalid_edge")
        if self.source == self.target:
            raise ValueError("self_edge_not_allowed")
        if not self.provenance.get("source"):
            raise ValueError("missing_provenance")

    def to_dict(self) -> dict:
        """Serialize the edge into its canonical persistent representation."""
        return asdict(self)
