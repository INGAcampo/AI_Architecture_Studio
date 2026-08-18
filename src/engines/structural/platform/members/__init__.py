from dataclasses import dataclass, field, replace
from enum import Enum
from math import dist

class MemberKind(str, Enum):
    COLUMN="column"
    BEAM="beam"
    BRACE="brace"
    CUSTOM="custom"

@dataclass(frozen=True, slots=True)
class MemberRelease:
    fx: bool=False; fy: bool=False; fz: bool=False
    mx: bool=False; my: bool=False; mz: bool=False

@dataclass(frozen=True, slots=True)
class StructuralMember:
    member_id: str
    kind: MemberKind
    start: tuple[float,float,float]
    end: tuple[float,float,float]
    section_id: str
    material_id: str
    start_release: MemberRelease = MemberRelease()
    end_release: MemberRelease = MemberRelease()
    rotation_degrees: float = 0.0
    metadata: dict = field(default_factory=dict)
    revision: int = 0

    def __post_init__(self):
        if not self.member_id.strip() or not self.section_id.strip() or not self.material_id.strip():
            raise ValueError("Campos obligatorios")
        if self.length <= 0:
            raise ValueError("Longitud inválida")

    @property
    def length(self):
        return dist(self.start,self.end)

    def with_end(self,end):
        return replace(self,end=tuple(end),revision=self.revision+1)

    def with_section(self,section_id):
        return replace(self,section_id=section_id,revision=self.revision+1)
