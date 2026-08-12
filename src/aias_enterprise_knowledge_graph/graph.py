"""Atomic graph persistence, traversal, impact analysis and controlled inference."""
from __future__ import annotations
import json, os, tempfile
from collections import deque
from pathlib import Path
from .models import Edge, Node
from .rules import RuleRegistry


class EnterpriseKnowledgeGraph:
    """Maintain the durable AIAS golden thread as typed nodes and edges."""
    def __init__(self, path: Path, rules: RuleRegistry | None = None):
        self.path = path
        self.rules = rules or RuleRegistry()
        self.data = self._load()

    def _load(self) -> dict:
        if not self.path.exists():
            return {"schema_version": "1.0.0", "nodes": {}, "edges": {}}
        return json.loads(self.path.read_text(encoding="utf-8"))

    def add_node(self, node: Node) -> dict:
        """Insert a unique node, allowing only idempotent identical replays."""
        node.validate(); row = node.to_dict(); old = self.data["nodes"].get(node.node_id)
        if old and old != row: raise ValueError("node_id_conflict")
        self.data["nodes"][node.node_id] = row; self._save(); return row

    def add_edge(self, edge: Edge) -> dict:
        """Insert an edge only when both endpoints exist and identity is unique."""
        edge.validate(); row = edge.to_dict()
        if edge.source not in self.data["nodes"] or edge.target not in self.data["nodes"]:
            raise ValueError("unknown_endpoint")
        old = self.data["edges"].get(edge.edge_id)
        if old and old != row: raise ValueError("edge_id_conflict")
        self.data["edges"][edge.edge_id] = row; self._save(); return row

    def related(self, node_id: str, direction: str = "both", relation: str | None = None) -> list[dict]:
        """Query incoming, outgoing or bidirectional adjacent relationships."""
        if direction not in {"incoming", "outgoing", "both"}: raise ValueError("invalid_direction")
        rows=[]
        for edge in self.data["edges"].values():
            matches = (direction in {"outgoing","both"} and edge["source"] == node_id) or (direction in {"incoming","both"} and edge["target"] == node_id)
            if matches and (relation is None or edge["relation"] == relation): rows.append(edge)
        return sorted(rows, key=lambda x: x["edge_id"])

    def shortest_path(self, source: str, target: str) -> list[str]:
        """Return the shortest directed node path or an empty list."""
        queue=deque([(source,[source])]); seen={source}
        while queue:
            current,path=queue.popleft()
            if current == target: return path
            for edge in self.related(current,"outgoing"):
                if edge["target"] not in seen: seen.add(edge["target"]);queue.append((edge["target"],path+[edge["target"]]))
        return []

    def impact(self, node_id: str) -> list[str]:
        """Return all transitively downstream concepts affected by one node."""
        seen=set();queue=deque([node_id])
        while queue:
            current=queue.popleft()
            for edge in self.related(current,"outgoing"):
                if edge["target"] not in seen: seen.add(edge["target"]);queue.append(edge["target"])
        seen.discard(node_id);return sorted(seen)

    def infer(self, rule_id: str) -> list[dict]:
        """Materialize only two-hop conclusions authorized by an approved rule."""
        rule=self.rules.approved(rule_id); created=[]
        left=[e for e in self.data["edges"].values() if e["relation"]==rule.left_relation]
        right=[e for e in self.data["edges"].values() if e["relation"]==rule.right_relation]
        for a in left:
            for b in right:
                if a["target"] == b["source"] and a["source"] != b["target"]:
                    eid=f"INF-{rule.rule_id}-{a['source']}-{b['target']}"
                    created.append(self.add_edge(Edge(eid,a["source"],rule.inferred_relation,b["target"],provenance={"source":"CONTROLLED_INFERENCE","rule_id":rule.rule_id,"supporting_edges":[a["edge_id"],b["edge_id"]]})))
        return created

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True,exist_ok=True);fd,name=tempfile.mkstemp(dir=self.path.parent,suffix=".tmp")
        try:
            with os.fdopen(fd,"w",encoding="utf-8") as stream: json.dump(self.data,stream,ensure_ascii=False,indent=2,sort_keys=True);stream.write("\n")
            os.replace(name,self.path)
        finally:
            if os.path.exists(name): os.unlink(name)
