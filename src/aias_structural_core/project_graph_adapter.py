"""Traceable structural projection from the canonical Project Graph.

This adapter is deliberately small: it defines the geometry/connectivity
contract consumed by the deterministic structural kernel without introducing
a second authoring model.  It is suitable for synthetic infrastructure tests,
not a substitute for a licensed engineering model or project inputs.
"""
from __future__ import annotations

from typing import Any

from aias_building_design_core import evidence_sha256


class ProjectGraphStructuralAdapter:
    """Project structural members and their endpoints from graph geometry."""

    structural_types = {"wall", "column", "beam", "slab", "foundation"}

    @staticmethod
    def _point(value: Any) -> list[float] | None:
        if not isinstance(value, (list, tuple)) or len(value) != 3:
            return None
        try:
            return [float(value[0]), float(value[1]), float(value[2])]
        except (TypeError, ValueError):
            return None

    def project(self, graph) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
        nodes_by_id = {node["id"]: node for node in graph.nodes}
        analysis_nodes: list[dict[str, Any]] = []
        members: list[dict[str, Any]] = []

        def add_node(member_id: str, role: str, xyz: list[float] | None, support: bool = False) -> str:
            node_id = f"analysis-node:{member_id}:{role}"
            # Fallback coordinates preserve deterministic test behaviour for a
            # legacy graph that did not yet own spatial geometry.
            if xyz is None:
                index = len(analysis_nodes)
                xyz = [float(index % 3) * 4.0, float(index // 3) * 4.0, 0.0]
                geometry_status = "LEGACY_GEOMETRY_FALLBACK"
            else:
                geometry_status = "PROJECT_GRAPH_GEOMETRY"
            analysis_nodes.append({
                "id": node_id, "source_node_id": member_id, "role": role,
                "xyz_m": xyz, "support": support,
                "geometry_status": geometry_status,
            })
            return node_id

        for item in graph.nodes:
            if item["type"] not in self.structural_types:
                continue
            props = item.get("properties", {})
            geometry = props.get("geometry", {})
            kind = geometry.get("kind")
            start = end = None
            if kind in {"linear_prism", "wall_extrusion"}:
                start = self._point(geometry.get("start_m") or geometry.get("baseline_start_m"))
                end = self._point(geometry.get("end_m") or geometry.get("baseline_end_m"))
            elif kind == "vertical_prism":
                start = self._point(geometry.get("base_point_m"))
                if start is not None:
                    end = [start[0], start[1], start[2] + float(geometry.get("height_m", props.get("height_m", 0.0)))]
            elif kind == "footing_prism":
                center = self._point(geometry.get("center_m"))
                if center is not None:
                    start = [center[0], center[1], 0.0]
                    end = start
            elif kind == "slab_extrusion":
                footprint = geometry.get("footprint_m", [])
                points = [self._point(point) for point in footprint]
                points = [point for point in points if point is not None]
                if points:
                    start = [sum(p[i] for p in points) / len(points) for i in range(3)]
                    end = start

            node_ids = [
                add_node(item["id"], "start", start, support=item["type"] == "foundation"),
                add_node(item["id"], "end", end, support=item["type"] == "foundation"),
            ]
            members.append({
                "id": item["id"], "type": item["type"], "material": "concrete",
                "source_node_id": item["id"], "node_ids": node_ids,
                "connectivity": {"start_node_id": node_ids[0], "end_node_id": node_ids[1]},
                "geometry_sha256": evidence_sha256(geometry),
                "geometry_status": "PROJECT_GRAPH_GEOMETRY" if start is not None else "LEGACY_GEOMETRY_FALLBACK",
            })

        metadata = {
            "source": "ProjectGraph",
            "source_graph_sha256": evidence_sha256(graph.to_dict()),
            "projection": "aias.project_graph_structural_adapter.v1",
            "member_count": len(members),
            "node_count": len(analysis_nodes),
            "geometry_backed_member_count": sum(m["geometry_status"] == "PROJECT_GRAPH_GEOMETRY" for m in members),
        }
        return analysis_nodes, members, metadata
