from dataclasses import dataclass
from enum import Enum
class SectionShape(str,Enum): RECTANGLE='rectangle'; CIRCLE='circle'; PIPE='pipe'; BOX='box'; I='i'; CHANNEL='channel'; ANGLE='angle'; CUSTOM='custom'
@dataclass(frozen=True,slots=True)
class StructuralSection:
 section_id:str; name:str; shape:SectionShape; dimensions:dict[str,float]; material_id:str
 def __post_init__(self):
  if not self.section_id.strip() or not self.name.strip() or not self.material_id.strip(): raise ValueError('Campos obligatorios')
  if not self.dimensions or any(v<=0 for v in self.dimensions.values()): raise ValueError('Dimensiones inválidas')
class StructuralSectionLibrary:
 def __init__(self): self._s={}
 def register(self,s,replace=False):
  if s.section_id in self._s and not replace: raise ValueError('Sección duplicada')
  self._s[s.section_id]=s; return s
 def get(self,i): return self._s[i]
 def by_shape(self,sh): return tuple(sorted((s for s in self._s.values() if s.shape is sh),key=lambda s:s.section_id))
