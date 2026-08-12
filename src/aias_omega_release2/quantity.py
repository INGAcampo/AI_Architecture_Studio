"""Public module supporting the second Omega integrated product release."""
from __future__ import annotations
from dataclasses import dataclass
from aias_omega_core.graph import Relationship
from aias_omega_core.objects import EngineeringObject
from aias_omega_core.project import EngineeringProject

@dataclass(frozen=True, slots=True)
class QuantityResult:
    """Execute the public QuantityResult operation for the second Omega integrated product release using explicit caller inputs."""
    length_m: float
    area_m2: float
    volume_m3: float
    unit_cost: float
    total_cost: float

class QuantityEngine:
    """Execute the public QuantityEngine operation for the second Omega integrated product release using explicit caller inputs."""
    def quantify_wall(self, wall: EngineeringObject, unit_cost_per_m3: float) -> QuantityResult:
        """Execute the public QuantityEngine.quantify_wall operation for the second Omega integrated product release using explicit caller inputs."""
        if wall.object_type != "bim_wall":
            raise TypeError("Expected bim_wall.")
        length = float(wall.properties["length_m"])
        height = float(wall.properties["height_m"])
        thickness = float(wall.properties["thickness_m"])
        area = length * height
        volume = area * thickness
        return QuantityResult(
            length_m=length,
            area_m2=area,
            volume_m3=volume,
            unit_cost=unit_cost_per_m3,
            total_cost=volume * unit_cost_per_m3,
        )

    def attach_wall_quantity(
        self,
        project: EngineeringProject,
        wall_object_id,
        unit_cost_per_m3: float,
    ):
        """Add wall quantity to the second Omega integrated product release while enforcing identity constraints."""
        wall = project.objects[wall_object_id]
        result = self.quantify_wall(wall, unit_cost_per_m3)
        item = EngineeringObject(
            object_type="quantity_item",
            name=f"Quantity {wall.name}",
            properties={
                "length_m": result.length_m,
                "area_m2": result.area_m2,
                "volume_m3": result.volume_m3,
                "unit_cost": result.unit_cost,
                "total_cost": result.total_cost,
            },
            material_id=wall.material_id,
            classification="Cost.Item",
        )
        item_id = project.add_object(item)
        project.graph.add(Relationship(wall_object_id, item_id, "quantified_by"))
        return item_id
