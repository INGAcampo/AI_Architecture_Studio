"""Public module supporting the second Omega integrated product release."""
from __future__ import annotations
from dataclasses import dataclass
from aias_omega_core.graph import Relationship
from aias_omega_core.objects import EngineeringObject
from aias_omega_core.project import EngineeringProject

@dataclass(frozen=True, slots=True)
class AxialBarInput:
    """Execute the public AxialBarInput operation for the second Omega integrated product release using explicit caller inputs."""
    length_m: float
    area_m2: float
    elastic_modulus_pa: float
    axial_load_n: float

@dataclass(frozen=True, slots=True)
class AxialBarResult:
    """Execute the public AxialBarResult operation for the second Omega integrated product release using explicit caller inputs."""
    displacement_m: float
    stress_pa: float
    strain: float
    reaction_n: float
    axial_stiffness_n_m: float

class AxialBarSolver:
    """Execute the public AxialBarSolver operation for the second Omega integrated product release using explicit caller inputs."""
    def solve(self, data: AxialBarInput) -> AxialBarResult:
        """Execute the public AxialBarSolver.solve operation for the second Omega integrated product release using explicit caller inputs."""
        if data.length_m <= 0:
            raise ValueError("Length must be positive.")
        if data.area_m2 <= 0:
            raise ValueError("Area must be positive.")
        if data.elastic_modulus_pa <= 0:
            raise ValueError("Elastic modulus must be positive.")

        stiffness = data.area_m2 * data.elastic_modulus_pa / data.length_m
        displacement = data.axial_load_n / stiffness
        stress = data.axial_load_n / data.area_m2
        strain = stress / data.elastic_modulus_pa
        return AxialBarResult(
            displacement_m=displacement,
            stress_pa=stress,
            strain=strain,
            reaction_n=-data.axial_load_n,
            axial_stiffness_n_m=stiffness,
        )

class StructuralAdapter:
    """Execute the public StructuralAdapter operation for the second Omega integrated product release using explicit caller inputs."""
    def wall_to_analytical_bar(
        self,
        project: EngineeringProject,
        wall_object_id,
        tributary_width_m: float = 1.0,
        load_n: float = 0.0,
    ):
        """Execute the public StructuralAdapter.wall_to_analytical_bar operation for the second Omega integrated product release using explicit caller inputs."""
        wall = project.objects[wall_object_id]
        if wall.object_type != "bim_wall":
            raise TypeError("Expected bim_wall.")

        length = float(wall.properties["length_m"])
        thickness = float(wall.properties["thickness_m"])
        area = thickness * tributary_width_m

        material = project.materials.get(wall.material_id)
        elastic_modulus_pa = float(material.properties["E_MPa"]) * 1_000_000.0

        result = AxialBarSolver().solve(AxialBarInput(
            length_m=length,
            area_m2=area,
            elastic_modulus_pa=elastic_modulus_pa,
            axial_load_n=load_n,
        ))

        analytical = EngineeringObject(
            object_type="structural_member",
            name=f"Analytical {wall.name}",
            geometry={"type": "bar", "length_m": length},
            properties={
                "area_m2": area,
                "elastic_modulus_pa": elastic_modulus_pa,
                "axial_load_n": load_n,
                "displacement_m": result.displacement_m,
                "stress_pa": result.stress_pa,
                "strain": result.strain,
                "reaction_n": result.reaction_n,
                "axial_stiffness_n_m": result.axial_stiffness_n_m,
            },
            material_id=wall.material_id,
            classification="Structural.Member",
        )
        analytical_id = project.add_object(analytical)
        project.graph.add(Relationship(
            wall_object_id,
            analytical_id,
            "analytical_representation",
        ))
        return analytical_id
