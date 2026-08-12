"""Public module supporting the second Omega integrated product release."""
from __future__ import annotations
from dataclasses import dataclass
from aias_omega_core.graph import Relationship
from aias_omega_core.objects import EngineeringObject
from aias_omega_core.project import EngineeringProject

@dataclass(frozen=True, slots=True)
class WallType:
    """Execute the public WallType operation for the second Omega integrated product release using explicit caller inputs."""
    name: str
    thickness_m: float
    height_m: float
    material_id: str

class CadToBimAdapter:
    """Execute the public CadToBimAdapter operation for the second Omega integrated product release using explicit caller inputs."""
    def line_to_wall(
        self,
        project: EngineeringProject,
        cad_object_id,
        wall_type: WallType,
        wall_name: str = "Wall",
    ):
        """Execute the public CadToBimAdapter.line_to_wall operation for the second Omega integrated product release using explicit caller inputs."""
        cad = project.objects[cad_object_id]
        if cad.object_type != "cad_line":
            raise TypeError("Expected cad_line.")

        start = cad.geometry["start"]
        end = cad.geometry["end"]
        dx = float(end[0]) - float(start[0])
        dy = float(end[1]) - float(start[1])
        length = (dx * dx + dy * dy) ** 0.5
        if length <= 0:
            raise ValueError("Wall axis must have positive length.")

        wall = EngineeringObject(
            object_type="bim_wall",
            name=wall_name,
            geometry={
                "type": "extruded_wall",
                "axis_start": list(start),
                "axis_end": list(end),
            },
            properties={
                "length_m": length,
                "height_m": wall_type.height_m,
                "thickness_m": wall_type.thickness_m,
            },
            material_id=wall_type.material_id,
            classification="BIM.Wall",
        )
        wall_id = project.add_object(wall)
        project.graph.add(Relationship(cad_object_id, wall_id, "generates"))
        return wall_id
