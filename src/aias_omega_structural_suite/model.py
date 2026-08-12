"""Nodes, materials, sections, elements, loads and complete planar structural models."""
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

@dataclass(frozen=True, slots=True)
class Node2D:
    """Planar frame node with translational and rotational restraint flags."""
    node_id: str
    x: float
    y: float
    restraint_x: bool = False
    restraint_y: bool = False
    restraint_rz: bool = False

@dataclass(frozen=True, slots=True)
class Material:
    """Linear-elastic structural material with modulus and density."""
    material_id: str
    elastic_modulus_pa: float
    yield_strength_pa: float
    density_kg_m3: float = 0.0

@dataclass(frozen=True, slots=True)
class Section:
    """Prismatic member section carrying area and second moment of area."""
    section_id: str
    area_m2: float
    inertia_m4: float
    depth_m: float = 0.0

@dataclass(frozen=True, slots=True)
class FrameElement2D:
    """Two-node planar frame member referencing material and section properties."""
    element_id: str
    node_i: str
    node_j: str
    material_id: str
    section_id: str

@dataclass(frozen=True, slots=True)
class NodalLoad2D:
    """Concentrated nodal force and moment vector."""
    node_id: str
    fx_n: float = 0.0
    fy_n: float = 0.0
    mz_nm: float = 0.0

@dataclass(slots=True)
class StructuralModel2D:
    """Validated aggregate of nodes, members and applied nodal loads."""
    nodes: Dict[str, Node2D] = field(default_factory=dict)
    materials: Dict[str, Material] = field(default_factory=dict)
    sections: Dict[str, Section] = field(default_factory=dict)
    elements: Dict[str, FrameElement2D] = field(default_factory=dict)
    loads: List[NodalLoad2D] = field(default_factory=list)

    def validate(self) -> None:
        """Validate validate for the Omega structural analysis and design suite and report explicit issues."""
        if not self.nodes:
            raise ValueError("Model has no nodes.")
        for e in self.elements.values():
            if e.node_i not in self.nodes or e.node_j not in self.nodes:
                raise ValueError(f"Element {e.element_id} references missing node.")
            if e.material_id not in self.materials:
                raise ValueError(f"Element {e.element_id} references missing material.")
            if e.section_id not in self.sections:
                raise ValueError(f"Element {e.element_id} references missing section.")
            ni, nj = self.nodes[e.node_i], self.nodes[e.node_j]
            if ni.x == nj.x and ni.y == nj.y:
                raise ValueError(f"Element {e.element_id} has zero length.")
