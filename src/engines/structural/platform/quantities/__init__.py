from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class MemberQuantities:
    length:float
    volume:float
    mass:float
    self_weight:float

class StructuralQuantityEngine:
    def calculate(self,member,section_properties,material):
        volume=member.length*section_properties.area
        mass=volume*material.density
        return MemberQuantities(member.length,volume,mass,mass*9.80665)
    def aggregate(self,items):
        return MemberQuantities(
            sum(i.length for i in items),
            sum(i.volume for i in items),
            sum(i.mass for i in items),
            sum(i.self_weight for i in items),
        )
