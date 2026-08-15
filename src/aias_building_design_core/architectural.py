"""Architectural production contract over the canonical Project Graph.

The graph remains the authoring source of truth.  This module validates and
projects it into traceable architectural evidence; it does not own a parallel
model.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, is_dataclass
from typing import Any


PIPELINE_ORDER = (
    "project_graph", "architecture", "native_bim", "analysis", "drawings",
    "quantities", "reports", "qa_qc", "issuance_manifest",
)


def evidence_sha256(value: Any) -> str:
    if is_dataclass(value):
        value = asdict(value)
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), default=str).encode()
    ).hexdigest()


class ArchitecturalProductionCore:
    """Validate spatial semantics and derive architectural evidence."""

    geometry_types = {
        "site", "grid", "level", "space", "wall", "door", "window",
        "column", "beam", "slab", "roof", "foundation",
    }

    def materialize(self, graph) -> dict[str, Any]:
        errors = self.validate(graph)
        if errors:
            raise ValueError("architectural graph invalid: " + "; ".join(errors))
        nodes = {node["id"]: node for node in graph.nodes}
        graph_sha = evidence_sha256(graph.to_dict())
        geometry_index = {
            node_id: {
                "source_node_id": node_id,
                "element_type": node["type"],
                "geometry": node["properties"]["geometry"],
                "geometry_sha256": evidence_sha256(node["properties"]["geometry"]),
            }
            for node_id, node in nodes.items()
            if node["type"] in self.geometry_types
        }
        host_by_opening = {
            rel["target"]: rel["source"]
            for rel in graph.relationships if rel["relation"] == "has_opening"
        }
        levels = []
        for level in sorted(
            (node for node in graph.nodes if node["type"] == "level"),
            key=lambda node: float(node["properties"]["elevation_m"]),
        ):
            contained = [
                rel["target"] for rel in graph.relationships
                if rel["source"] == level["id"] and rel["relation"] == "contains"
            ]
            levels.append({
                "level_id": level["id"],
                "elevation_m": float(level["properties"]["elevation_m"]),
                "height_m": float(level["properties"]["height_m"]),
                "spaces": sorted(x for x in contained if nodes[x]["type"] == "space"),
                "envelope_walls": sorted(
                    x for x in contained
                    if nodes[x]["type"] == "wall" and nodes[x]["properties"].get("exterior")
                ),
                "openings": sorted(x for x in contained if nodes[x]["type"] in {"door", "window"}),
            })
        walls = [node for node in graph.nodes if node["type"] == "wall" and node["properties"].get("exterior")]
        openings = [node for node in graph.nodes if node["type"] in {"door", "window"}]
        gross_wall_area = sum(float(n["properties"]["length_m"]) * float(n["properties"]["height_m"]) for n in walls)
        opening_area = sum(float(n["properties"]["width_m"]) * float(n["properties"]["height_m"]) for n in openings)
        roof_area = sum(float(n["properties"].get("area_m2", 0.0)) for n in graph.nodes if n["type"] == "roof")
        return {
            "schema": "aias.architectural_production_core.v1",
            "project_id": graph.project_id,
            "source": "ProjectGraph",
            "source_graph_sha256": graph_sha,
            "levels": levels,
            "grids": sorted(node["id"] for node in graph.nodes if node["type"] == "grid"),
            "spaces": sorted(node["id"] for node in graph.nodes if node["type"] == "space"),
            "envelope": {
                "wall_ids": sorted(node["id"] for node in walls),
                "roof_ids": sorted(node["id"] for node in graph.nodes if node["type"] == "roof"),
                "gross_wall_area_m2": gross_wall_area,
                "opening_area_m2": opening_area,
                "net_wall_area_m2": gross_wall_area - opening_area,
                "roof_area_m2": roof_area,
            },
            "openings": {
                node["id"]: {"host_wall_id": host_by_opening[node["id"]], "geometry_sha256": geometry_index[node["id"]]["geometry_sha256"]}
                for node in openings
            },
            "geometry_index": geometry_index,
            "relationship_sha256": evidence_sha256(graph.relationships),
            "traceability": {"authoring_source": "ProjectGraph", "node_ids": sorted(nodes)},
        }

    def validate(self, graph) -> list[str]:
        errors: list[str] = []
        nodes = {node["id"]: node for node in graph.nodes}
        if len(nodes) != len(graph.nodes):
            errors.append("duplicate node ids")
        relationships = graph.relationships
        levels = [node for node in graph.nodes if node["type"] == "level"]
        grids = [node for node in graph.nodes if node["type"] == "grid"]
        if not levels:
            errors.append("at least one level is required")
        if len(grids) < 4:
            errors.append("at least four boundary grids are required")
        axes = [node["properties"].get("axis") for node in grids]
        if None in axes or len(axes) != len(set(axes)):
            errors.append("grid axes must be present and unique")
        for relation in relationships:
            if relation.get("source") not in nodes or relation.get("target") not in nodes:
                errors.append("dangling architectural relationship")
        for node in graph.nodes:
            if node["type"] in self.geometry_types and not node.get("properties", {}).get("geometry"):
                errors.append(f"{node['id']} has no traceable geometry")
        containment = {
            rel["target"]: rel["source"]
            for rel in relationships if rel["relation"] == "contains"
        }
        for level in levels:
            children = [
                nodes[rel["target"]] for rel in relationships
                if rel["source"] == level["id"]
                and rel["relation"] == "contains"
                and rel["target"] in nodes
            ]
            spaces = [node for node in children if node["type"] == "space"]
            walls = [node for node in children if node["type"] == "wall"]
            if not spaces:
                errors.append(f"{level['id']} contains no space")
            if len(walls) < 4:
                errors.append(f"{level['id']} has an incomplete envelope")
            wall_ids = {node["id"] for node in walls}
            for space in spaces:
                boundaries = {
                    rel["target"] for rel in relationships
                    if rel["source"] == space["id"] and rel["relation"] == "bounded_by"
                }
                if len(boundaries & wall_ids) < 4:
                    errors.append(f"{space['id']} has incomplete spatial boundaries")
                access = {
                    rel["target"] for rel in relationships
                    if rel["source"] == space["id"] and rel["relation"] == "accessed_by"
                }
                daylight = {
                    rel["target"] for rel in relationships
                    if rel["source"] == space["id"] and rel["relation"] == "daylit_by"
                }
                if not access or not all(nodes.get(x, {}).get("type") == "door" for x in access):
                    errors.append(f"{space['id']} has no valid access relationship")
                if not daylight or not all(nodes.get(x, {}).get("type") == "window" for x in daylight):
                    errors.append(f"{space['id']} has no valid daylight relationship")
        host_relations: dict[str, list[str]] = {}
        for rel in relationships:
            if rel["relation"] == "has_opening":
                host_relations.setdefault(rel["target"], []).append(rel["source"])
        for opening in (node for node in graph.nodes if node["type"] in {"door", "window"}):
            hosts = host_relations.get(opening["id"], [])
            if len(hosts) != 1 or hosts[0] not in nodes or nodes[hosts[0]]["type"] != "wall":
                errors.append(f"{opening['id']} must have exactly one wall host")
                continue
            if containment.get(opening["id"]) != containment.get(hosts[0]):
                errors.append(f"{opening['id']} and host wall must share a level")
            wall_length = float(nodes[hosts[0]]["properties"].get("length_m", 0.0))
            wall_height = float(nodes[hosts[0]]["properties"].get("height_m", 0.0))
            props = opening["properties"]
            if float(props.get("offset_m", -1.0)) < 0 or float(props.get("offset_m", 0.0)) + float(props.get("width_m", 0.0)) > wall_length:
                errors.append(f"{opening['id']} exceeds its host wall")
            sill = float(props.get("sill_height_m", 0.0))
            if sill < 0 or sill + float(props.get("height_m", 0.0)) > wall_height:
                errors.append(f"{opening['id']} exceeds its host wall height")
            geometry_host = props.get("geometry", {}).get("host_wall_id")
            if geometry_host != hosts[0]:
                errors.append(f"{opening['id']} geometry host does not match relationship host")
        for host_id, opening_ids in host_relations.items():
            intervals = sorted(
                (
                    float(nodes[x]["properties"].get("offset_m", 0.0)),
                    float(nodes[x]["properties"].get("offset_m", 0.0))
                    + float(nodes[x]["properties"].get("width_m", 0.0)),
                    x,
                )
                for x in opening_ids if x in nodes
            )
            for previous, current in zip(intervals, intervals[1:]):
                if current[0] < previous[1]:
                    errors.append(
                        f"{previous[2]} and {current[2]} overlap on host {host_id}"
                    )
        walls = [node for node in graph.nodes if node["type"] == "wall" and node["properties"].get("exterior")]
        gross_area = sum(float(node["properties"].get("length_m", 0.0)) * float(node["properties"].get("height_m", 0.0)) for node in walls)
        opening_area = sum(float(node["properties"].get("width_m", 0.0)) * float(node["properties"].get("height_m", 0.0)) for node in graph.nodes if node["type"] in {"door", "window"})
        if opening_area >= gross_area:
            errors.append("envelope openings exceed gross wall area")
        return errors

    def verify_coherence(self, graph, architecture, analysis_model, drawing_model, quantities, native_bim=None) -> dict[str, Any]:
        project_ids = {graph.project_id, architecture.get("project_id"), analysis_model.project_id, drawing_model.project_id, quantities.project_id}
        if native_bim is not None:
            project_ids.add(native_bim.get("project_id"))
        graph_ids = {node["id"] for node in graph.nodes}
        structural_ids = {node["id"] for node in graph.nodes if node["type"] in {"wall", "column", "beam", "slab", "foundation"}}
        analysis_ids = {member["id"] for member in analysis_model.members}
        drawing_ids = set().union(*(set(view.get("source_node_ids", ())) for view in drawing_model.views)) if drawing_model.views else set()
        quantifiable_ids = {node["id"] for node in graph.nodes if node["type"] in {"wall", "slab", "door", "window", "foundation"}}
        quantity_ids = {item["element_id"] for item in quantities.items}
        geometry_ids = set(architecture.get("geometry_index", {}))
        graph_sha = architecture.get("source_graph_sha256")
        analysis_geometry = {
            member["source_node_id"]: member.get("geometry_sha256")
            for member in analysis_model.members
        }
        drawing_geometry = drawing_model.views[0].get("source_geometry_sha256", {}) if drawing_model.views else {}
        quantity_geometry = {
            item["element_id"]: item.get("source_geometry_sha256")
            for item in quantities.items
        }
        checks = {
            "project_identity": len(project_ids) == 1,
            "native_bim_graph_binding": native_bim is not None and (
                native_bim.get("traceability", {}).get("source_graph_sha256") == graph_sha
            ),
            "native_bim_wall_coverage": native_bim is not None and (
                set(native_bim.get("walls", {}))
                == {node["id"] for node in graph.nodes if node["type"] == "wall"}
            ),
            "analysis_members": analysis_ids == structural_ids,
            "drawing_coverage": graph_ids <= drawing_ids,
            "quantity_coverage": quantity_ids == quantifiable_ids,
            "geometry_traceability": quantifiable_ids <= geometry_ids,
            "analysis_geometry_binding": all(
                analysis_geometry.get(node_id) == architecture["geometry_index"][node_id]["geometry_sha256"]
                for node_id in structural_ids
            ),
            "drawing_geometry_binding": all(
                drawing_geometry.get(node_id) == architecture["geometry_index"][node_id]["geometry_sha256"]
                for node_id in graph_ids if node_id in geometry_ids
            ),
            "quantity_geometry_binding": all(
                quantity_geometry.get(node_id) == architecture["geometry_index"][node_id]["geometry_sha256"]
                for node_id in quantifiable_ids
            ),
            "analysis_graph_binding": analysis_model.metadata.get("source_graph_sha256") == graph_sha,
            "drawing_graph_binding": all(view.get("source_graph_sha256") == graph_sha for view in drawing_model.views),
            "quantity_graph_binding": all(item.get("source_graph_sha256") == graph_sha for item in quantities.items),
        }
        return {
            "schema": "aias.bim_analysis_drawings_quantities_coherence.v1",
            "project_id": graph.project_id,
            "checks": checks,
            "coverage": {"graph": len(graph_ids), "analysis": len(analysis_ids), "drawings": len(drawing_ids), "quantities": len(quantity_ids)},
            "source_graph_sha256": architecture.get("source_graph_sha256"),
            "verdict": "ARCHITECTURAL_PIPELINE_COHERENT" if all(checks.values()) else "FAIL",
        }

    def plan_selective_regeneration(self, before, after) -> dict[str, Any]:
        if before.project_id != after.project_id:
            raise ValueError("selective regeneration cannot cross project boundaries")
        before_nodes = {node["id"]: node for node in before.nodes}
        after_nodes = {node["id"]: node for node in after.nodes}
        changed = {
            node_id for node_id in set(before_nodes) | set(after_nodes)
            if before_nodes.get(node_id) != after_nodes.get(node_id)
        }
        before_rel = {json.dumps(rel, sort_keys=True) for rel in before.relationships}
        after_rel = {json.dumps(rel, sort_keys=True) for rel in after.relationships}
        for encoded in before_rel ^ after_rel:
            rel = json.loads(encoded)
            changed.update((rel["source"], rel["target"]))
        changed_types = {
            (after_nodes.get(node_id) or before_nodes[node_id])["type"] for node_id in changed
        }
        invalidated = {"project_graph"} if changed else set()
        if changed_types & {"site", "grid", "level", "space", "wall", "slab", "roof"}:
            invalidated.update(PIPELINE_ORDER[1:])
        if changed_types & {"door", "window"}:
            invalidated.update(("architecture", "native_bim", "drawings", "quantities", "reports", "qa_qc", "issuance_manifest"))
        if changed_types & {"column", "beam", "foundation"}:
            invalidated.update(("architecture", "analysis", "drawings", "quantities", "reports", "qa_qc", "issuance_manifest"))
        if changed_types & {"material"}:
            invalidated.update(("analysis", "quantities", "reports", "qa_qc", "issuance_manifest"))
        ordered = [stage for stage in PIPELINE_ORDER if stage in invalidated]
        return {
            "schema": "aias.project_selective_regeneration_plan.v1",
            "project_id": after.project_id,
            "graph_before_sha256": evidence_sha256(before.to_dict()),
            "graph_after_sha256": evidence_sha256(after.to_dict()),
            "changed": bool(changed),
            "changed_node_ids": sorted(changed),
            "changed_types": sorted(changed_types),
            "order": ordered,
            "preserved": [stage for stage in PIPELINE_ORDER if stage not in invalidated],
        }
