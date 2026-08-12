from dataclasses import dataclass
from engines.structural.platform.members import StructuralMember,MemberKind

@dataclass(frozen=True,slots=True)
class ColumnConstraints:
    base_level_id:str
    top_level_id:str
    base_offset:float=0.0
    top_offset:float=0.0
    effective_length_factor:float=1.0

@dataclass(frozen=True,slots=True)
class ColumnInstance:
    member:StructuralMember
    constraints:ColumnConstraints
    family_id:str
    type_id:str

    def __post_init__(self):
        if self.member.kind is not MemberKind.COLUMN:
            raise ValueError("El miembro debe ser columna")

class NativeBimColumnEngine:
    def axial_length(self,column): return column.member.length*column.constraints.effective_length_factor
    def self_weight(self,column,section_properties,material):
        return section_properties.area*column.member.length*material.density*9.80665
    def slenderness(self,column,section_properties):
        return self.axial_length(column)/min(section_properties.rx,section_properties.ry)
    def validate(self,column,section_properties):
        issues=[]
        if self.slenderness(column,section_properties)>200: issues.append("high_slenderness")
        if abs(column.member.start[0]-column.member.end[0])>1e-9 or abs(column.member.start[1]-column.member.end[1])>1e-9:
            issues.append("inclined_column")
        return tuple(issues)
