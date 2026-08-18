"""Parametric Project Graph authoring for isolated production projects."""
from __future__ import annotations

from aias_building_design_core import BuildingDesignCore


def _rectangle(width: float, length: float, elevation: float) -> list[list[float]]:
    return [
        [0.0, 0.0, elevation],
        [width, 0.0, elevation],
        [width, length, elevation],
        [0.0, length, elevation],
    ]


class ParametricProjectGraphBuilder:
    """Build an isolated architectural/structural graph from validated intake."""

    def build(self, manifest):
        from aias_project_intake import ProjectIntake

        intake = ProjectIntake().validate(manifest)
        program = intake["program"]
        core = BuildingDesignCore()
        graph = core.create_project(manifest["project_name"], project_id=manifest["project_id"])
        width = float(program["width_m"])
        length = float(program["length_m"])
        height = float(program["storey_height_m"])
        level_count = int(program["levels"])

        graph.add_node(
            "site",
            "Site",
            id="site-001",
            width_m=width,
            length_m=length,
            units="SI",
            geometry={
                "kind": "planar_rectangle",
                "vertices_m": _rectangle(width, length, 0.0),
            },
        )
        graph.add_node("material", "Concrete", id="material-concrete", grade="C25/30")

        grid_lines = {
            "A": ([0.0, 0.0, 0.0], [0.0, length, 0.0], 0.0),
            "B": ([width, 0.0, 0.0], [width, length, 0.0], width),
            "1": ([0.0, 0.0, 0.0], [width, 0.0, 0.0], 0.0),
            "2": ([0.0, length, 0.0], [width, length, 0.0], length),
        }
        for axis, (start, end, coordinate) in grid_lines.items():
            grid_id = f"grid-{axis}"
            graph.add_node(
                "grid",
                f"Grid {axis}",
                id=grid_id,
                axis=axis,
                coordinate_m=coordinate,
                geometry={"kind": "line", "start_m": start, "end_m": end},
            )
            graph.relate("site-001", "contains", grid_id)

        wall_lines = {
            "north": ([0.0, length], [width, length], width),
            "south": ([0.0, 0.0], [width, 0.0], width),
            "east": ([width, 0.0], [width, length], length),
            "west": ([0.0, 0.0], [0.0, length], length),
        }
        corner_points = {
            "A1": [0.0, 0.0],
            "A2": [0.0, length],
            "B1": [width, 0.0],
            "B2": [width, length],
        }
        beam_lines = {
            "A": ([0.0, 0.0], [0.0, length], length),
            "B": ([width, 0.0], [width, length], length),
            "1": ([0.0, 0.0], [width, 0.0], width),
            "2": ([0.0, length], [width, length], width),
        }

        for index in range(level_count):
            number = index + 1
            elevation = index * height
            level_id = f"level-{number:02d}"
            graph.add_node(
                "level",
                f"Level {number}",
                id=level_id,
                elevation_m=elevation,
                height_m=height,
                geometry={
                    "kind": "datum_plane",
                    "elevation_m": elevation,
                    "outline_m": _rectangle(width, length, elevation),
                },
            )
            graph.relate("site-001", "contains", level_id)

            space_id = f"space-{number:02d}"
            graph.add_node(
                "space",
                f"Floor {number}",
                id=space_id,
                area_m2=width * length,
                volume_m3=width * length * height,
                geometry={
                    "kind": "extruded_polygon",
                    "footprint_m": _rectangle(width, length, elevation),
                    "height_m": height,
                },
            )
            graph.relate(level_id, "contains", space_id)

            slab_id = f"slab-{number:02d}"
            graph.add_node(
                "slab",
                f"Slab {number}",
                id=slab_id,
                area_m2=width * length,
                thickness_m=0.15,
                geometry={
                    "kind": "slab_extrusion",
                    "footprint_m": _rectangle(width, length, elevation),
                    "thickness_m": 0.15,
                },
            )
            graph.relate(level_id, "contains", slab_id)
            graph.relate(slab_id, "uses_material", "material-concrete")

            for side, (start_xy, end_xy, wall_length) in wall_lines.items():
                wall_id = f"wall-{number:02d}-{side}"
                start = [start_xy[0], start_xy[1], elevation]
                end = [end_xy[0], end_xy[1], elevation]
                graph.add_node(
                    "wall",
                    f"Wall {number} {side}",
                    id=wall_id,
                    length_m=wall_length,
                    height_m=height,
                    thickness_m=0.20,
                    exterior=True,
                    geometry={
                        "kind": "wall_extrusion",
                        "baseline_start_m": start,
                        "baseline_end_m": end,
                        "height_m": height,
                        "thickness_m": 0.20,
                    },
                )
                graph.relate(level_id, "contains", wall_id)
                graph.relate(space_id, "bounded_by", wall_id)
                graph.relate(wall_id, "uses_material", "material-concrete")

            for corner, point in corner_points.items():
                column_id = f"column-{number:02d}-{corner}"
                graph.add_node(
                    "column",
                    f"Column {number} {corner}",
                    id=column_id,
                    width_m=0.30,
                    depth_m=0.30,
                    height_m=height,
                    geometry={
                        "kind": "vertical_prism",
                        "base_point_m": [point[0], point[1], elevation],
                        "width_m": 0.30,
                        "depth_m": 0.30,
                        "height_m": height,
                    },
                )
                graph.relate(level_id, "contains", column_id)
                graph.relate(column_id, "uses_material", "material-concrete")

            for edge, (start_xy, end_xy, beam_length) in beam_lines.items():
                beam_id = f"beam-{number:02d}-{edge}"
                graph.add_node(
                    "beam",
                    f"Beam {number} {edge}",
                    id=beam_id,
                    length_m=beam_length,
                    width_m=0.30,
                    depth_m=0.50,
                    geometry={
                        "kind": "linear_prism",
                        "start_m": [start_xy[0], start_xy[1], elevation + height],
                        "end_m": [end_xy[0], end_xy[1], elevation + height],
                        "width_m": 0.30,
                        "depth_m": 0.50,
                    },
                )
                graph.relate(level_id, "contains", beam_id)
                graph.relate(beam_id, "uses_material", "material-concrete")

            door_id = f"door-{number:02d}-01"
            window_id = f"window-{number:02d}-01"
            door_offset = min(0.50, max(0.10, width - 1.00))
            window_offset = max(0.10, (width - 1.20) / 2.0)
            graph.add_node(
                "door",
                f"Door {number}",
                id=door_id,
                width_m=0.90,
                height_m=2.10,
                offset_m=door_offset,
                sill_height_m=0.0,
                geometry={
                    "kind": "hosted_opening",
                    "host_wall_id": f"wall-{number:02d}-south",
                    "offset_m": door_offset,
                    "width_m": 0.90,
                    "height_m": 2.10,
                    "sill_height_m": 0.0,
                },
            )
            graph.add_node(
                "window",
                f"Window {number}",
                id=window_id,
                width_m=1.20,
                height_m=1.20,
                offset_m=window_offset,
                sill_height_m=0.90,
                geometry={
                    "kind": "hosted_opening",
                    "host_wall_id": f"wall-{number:02d}-north",
                    "offset_m": window_offset,
                    "width_m": 1.20,
                    "height_m": 1.20,
                    "sill_height_m": 0.90,
                },
            )
            for opening_id in (door_id, window_id):
                graph.relate(level_id, "contains", opening_id)
            graph.relate(f"wall-{number:02d}-south", "has_opening", door_id)
            graph.relate(f"wall-{number:02d}-north", "has_opening", window_id)
            graph.relate(space_id, "accessed_by", door_id)
            graph.relate(space_id, "daylit_by", window_id)

        for corner, point in corner_points.items():
            foundation_id = f"foundation-{corner}"
            graph.add_node(
                "foundation",
                f"Foundation {corner}",
                id=foundation_id,
                system="isolated",
                width_m=1.20,
                length_m=1.20,
                depth_m=0.40,
                geometry={
                    "kind": "footing_prism",
                    "center_m": [point[0], point[1], -0.40],
                    "width_m": 1.20,
                    "length_m": 1.20,
                    "depth_m": 0.40,
                },
            )
            graph.relate("site-001", "supports", foundation_id)
            graph.relate(foundation_id, "uses_material", "material-concrete")

        roof_elevation = level_count * height
        graph.add_node(
            "roof",
            "Roof",
            id="roof-001",
            area_m2=width * length,
            geometry={
                "kind": "roof_plane",
                "outline_m": _rectangle(width, length, roof_elevation),
                "elevation_m": roof_elevation,
            },
        )
        graph.relate(f"level-{level_count:02d}", "contains", "roof-001")

        errors = core.validate(graph)
        if errors:
            raise ValueError("; ".join(errors))
        return graph
