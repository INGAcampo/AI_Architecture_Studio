"""Immediate enterprise-graph consumers for existing governed AIAS assets."""
from __future__ import annotations
import json
from pathlib import Path
from .graph import EnterpriseKnowledgeGraph
from .models import Edge, Node


def import_master_inventory(graph: EnterpriseKnowledgeGraph, inventory_path: Path) -> dict:
    """Import the canonical AMIR concepts and dependencies with file provenance."""
    payload=json.loads(inventory_path.read_text(encoding="utf-8")); concepts=payload.get("concepts",payload.get("items",[]));edges=0
    for item in concepts:
        graph.add_node(Node(item["id"],item.get("kind","CONCEPT"),item["name"],properties={"state":item.get("declared_state"),"wave":item.get("wave")},provenance={"source":str(inventory_path)}))
    for item in concepts:
        for dependency in item.get("depends_on",[]):
            if dependency in graph.data["nodes"]:
                graph.add_edge(Edge(f"DEP-{item['id']}-{dependency}",dependency,"enables",item["id"],provenance={"source":str(inventory_path)}));edges+=1
    return {"nodes":len(concepts),"edges":edges}
