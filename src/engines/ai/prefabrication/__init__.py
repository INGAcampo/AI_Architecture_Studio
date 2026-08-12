from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class AssemblyPart:
    part_id:str;quantity:int;unit_mass:float
@dataclass(frozen=True,slots=True)
class AssemblyDefinition:
    assembly_id:str;parts:tuple[AssemblyPart,...]
class PrefabricationEngine:
    def total_parts(self,a): return sum(p.quantity for p in a.parts)
    def total_mass(self,a): return sum(p.quantity*p.unit_mass for p in a.parts)
    def bill_of_materials(self,a): return {p.part_id:p.quantity for p in a.parts}
