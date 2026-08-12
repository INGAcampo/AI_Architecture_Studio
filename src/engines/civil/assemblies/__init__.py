from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Subassembly:
    subassembly_id: str
    width: float
    slope: float
    code: str

@dataclass(frozen=True, slots=True)
class Assembly:
    assembly_id: str
    subassemblies: tuple[Subassembly, ...]

class AssemblyEngine:
    def total_width(self, assembly):
        return sum(item.width for item in assembly.subassemblies)

    def codes(self, assembly):
        return tuple(item.code for item in assembly.subassemblies)
