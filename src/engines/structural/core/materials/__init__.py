from dataclasses import dataclass
from enum import Enum
class MaterialCategory(str,Enum): CONCRETE='concrete'; STEEL='steel'; TIMBER='timber'; COMPOSITE='composite'; CUSTOM='custom'
@dataclass(frozen=True,slots=True)
class StructuralMaterial:
 material_id:str; name:str; category:MaterialCategory; elastic_modulus:float; shear_modulus:float; poisson_ratio:float; density:float; thermal_expansion:float=0.; yield_strength:float=0.; ultimate_strength:float=0.; compressive_strength:float=0.
 def __post_init__(self):
  if not self.material_id.strip() or not self.name.strip(): raise ValueError('IDs obligatorios')
  if self.elastic_modulus<=0 or self.shear_modulus<=0 or self.density<=0: raise ValueError('Propiedades inválidas')
class StructuralMaterialLibrary:
 def __init__(self): self._m={}
 def register(self,m,replace=False):
  if m.material_id in self._m and not replace: raise ValueError('Material duplicado')
  self._m[m.material_id]=m; return m
 def get(self,i): return self._m[i]
 def by_category(self,c): return tuple(sorted((m for m in self._m.values() if m.category is c),key=lambda m:m.material_id))
