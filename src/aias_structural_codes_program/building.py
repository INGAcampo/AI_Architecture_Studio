"""Canonical, software-neutral structural building contract for BIM/CAE consumers."""
from __future__ import annotations
from dataclasses import asdict,dataclass

@dataclass(frozen=True,slots=True)
class BuildingNode:
    node_id:str;x_m:float;y_m:float;z_m:float

@dataclass(frozen=True,slots=True)
class StructuralMember:
    member_id:str;kind:str;start_node:str;end_node:str;material_id:str;section_id:str

@dataclass(frozen=True,slots=True)
class StructuralBuilding:
    project_id:str;building_id:str;revision:str;coordinate_reference:str;unit_system:str;nodes:tuple[BuildingNode,...];members:tuple[StructuralMember,...];jurisdiction_pack_id:str|None=None
    def validate(self)->list[str]:
        issues=[];node_ids=[x.node_id for x in self.nodes];member_ids=[x.member_id for x in self.members]
        if len(node_ids)!=len(set(node_ids)):issues.append("duplicate_node_id")
        if len(member_ids)!=len(set(member_ids)):issues.append("duplicate_member_id")
        known=set(node_ids)
        for m in self.members:
            if m.kind not in {"BEAM","COLUMN","BRACE","WALL","SLAB","FOUNDATION"}:issues.append(f"{m.member_id}:unsupported_kind")
            if m.start_node not in known or m.end_node not in known:issues.append(f"{m.member_id}:unknown_node")
            if m.start_node==m.end_node:issues.append(f"{m.member_id}:zero_topology")
        if self.unit_system!="SI":issues.append("unsupported_unit_system")
        if not self.coordinate_reference:issues.append("coordinate_reference_required")
        return issues
    def exchange(self)->dict:
        """Project stable BIM/CAE data without claiming vendor-native conformance."""
        return {"schema":"AIAS-STRUCTURAL-BUILDING-1.0","building":asdict(self),"review_status":"FOR_ENGINEERING_REVIEW","normative_status":"JURISDICTION_PACK_REQUIRED" if not self.jurisdiction_pack_id else "PACK_DECLARED_NOT_YET_APPROVED","construction_approved":False}
