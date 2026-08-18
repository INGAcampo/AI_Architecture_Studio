"""Public module supporting the Omega application core and shared runtime services."""
from __future__ import annotations
from .graph import Relationship
from .materials import Material
from .objects import EngineeringObject
from .project import EngineeringProject

def create_cad_to_bim_to_structural_demo() -> EngineeringProject:
    """Build the cad to bim to structural demo required by the Omega application core and shared runtime services from explicit inputs."""
    project = EngineeringProject("Omega Demo")

    concrete = Material(
        "CONC_30",
        "Concrete 30 MPa",
        "concrete",
        {"E_MPa": 30000.0, "density_kg_m3": 2400.0},
    )
    project.materials.add(concrete)

    cad_axis = EngineeringObject(
        object_type="cad_line",
        name="Wall Axis",
        geometry={"type": "line", "start": [0.0, 0.0], "end": [5.0, 0.0]},
        classification="CAD.Axis",
    )
    cad_id = project.add_object(cad_axis)

    wall = EngineeringObject(
        object_type="bim_wall",
        name="Wall W01",
        geometry={"type": "extruded_wall", "axis_object_id": str(cad_id)},
        properties={"height_m": 3.0, "thickness_m": 0.20, "length_m": 5.0},
        material_id="CONC_30",
        classification="BIM.Wall",
    )
    wall_id = project.add_object(wall)
    project.graph.add(Relationship(cad_id, wall_id, "generates"))

    analytical = EngineeringObject(
        object_type="structural_member",
        name="Analytical Wall Strip",
        geometry={"type": "bar", "length_m": 5.0},
        properties={"area_m2": 0.60, "load_kN": 25.0},
        material_id="CONC_30",
        classification="Structural.Member",
    )
    analytical_id = project.add_object(analytical)
    project.graph.add(Relationship(wall_id, analytical_id, "analytical_representation"))

    quantity = EngineeringObject(
        object_type="quantity_item",
        name="Wall Concrete",
        properties={
            "volume_m3": 5.0 * 3.0 * 0.20,
            "unit_cost": 180.0,
            "total_cost": 5.0 * 3.0 * 0.20 * 180.0,
        },
        classification="Cost.Item",
    )
    quantity_id = project.add_object(quantity)
    project.graph.add(Relationship(wall_id, quantity_id, "quantified_by"))

    return project
