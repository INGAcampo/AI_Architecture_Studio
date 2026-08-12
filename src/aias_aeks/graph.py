"""Knowledge-unit dependency graph construction and cycle detection."""
from __future__ import annotations
from .models import KnowledgeUnit
from .ontology import OntologyGraph

class KnowledgeGraphBuilder:
    """Project registered knowledge and references into a validated directed graph."""
    def build(self, units: list[KnowledgeUnit]) -> OntologyGraph:
        """Build typed reference relationships between supplied knowledge units."""
        graph = OntologyGraph()
        for unit in units:
            graph.add(unit.eku_id, "is_a", unit.category)
            graph.add(unit.eku_id, "belongs_to", unit.discipline)
            for rel in unit.relationships:
                graph.add(unit.eku_id, rel["type"], rel["target"])
            for standard in unit.content.get("standards", []):
                graph.add(unit.eku_id, "uses_standard", standard)
        return graph
