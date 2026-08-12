from dataclasses import dataclass
from engines.structural.platform.members import StructuralMember,MemberKind

@dataclass(frozen=True,slots=True)
class BeamOffsets:
    start_y:float=0.0;start_z:float=0.0;end_y:float=0.0;end_z:float=0.0

@dataclass(frozen=True,slots=True)
class BeamInstance:
    member:StructuralMember
    family_id:str
    type_id:str
    offsets:BeamOffsets=BeamOffsets()

    def __post_init__(self):
        if self.member.kind is not MemberKind.BEAM:
            raise ValueError("El miembro debe ser viga")

class NativeBimBeamEngine:
    def span(self,beam): return beam.member.length
    def self_weight(self,beam,section_properties,material):
        return section_properties.area*beam.member.length*material.density*9.80665
    def line_weight(self,beam,section_properties,material):
        return section_properties.area*material.density*9.80665
    def validate(self,beam):
        issues=[]
        if abs(beam.member.end[2]-beam.member.start[2])>1e-6: issues.append("sloped_beam")
        if beam.member.length<0.5: issues.append("short_beam")
        return tuple(issues)
