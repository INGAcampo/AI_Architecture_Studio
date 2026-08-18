from dataclasses import dataclass
from typing import Protocol, runtime_checkable

@runtime_checkable
class FiniteElement(Protocol):
    element_id: str
    node_ids: tuple[str, ...]
    def local_stiffness_matrix(self): ...
    def transformation_matrix(self): ...
    def equivalent_nodal_loads(self): ...
    def recover_internal_forces(self, local_displacements): ...

@dataclass(frozen=True, slots=True)
class ElementMetadata:
    element_id: str
    element_type: str
    node_ids: tuple[str, ...]
    material_id: str
    section_id: str | None = None

class FiniteElementValidator:
    def validate(self, element):
        issues=[]
        if not getattr(element,"element_id",""): issues.append("missing_element_id")
        if len(getattr(element,"node_ids",()))<2: issues.append("insufficient_nodes")
        for name in ("local_stiffness_matrix","transformation_matrix","equivalent_nodal_loads","recover_internal_forces"):
            if not callable(getattr(element,name,None)): issues.append(f"missing_{name}")
        return tuple(issues)
