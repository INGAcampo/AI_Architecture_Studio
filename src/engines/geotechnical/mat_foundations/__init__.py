from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ColumnLoad: column_id:str; x:float; y:float; vertical_load:float
@dataclass(frozen=True,slots=True)
class MatFoundation:
    mat_id:str; width:float; length:float; thickness:float; column_loads:tuple; subgrade_modulus:float
    @property
    def area(self): return self.width*self.length
class MatFoundationEngine:
    def total_load(self,m): return sum(x.vertical_load for x in m.column_loads)
    def average_contact_pressure(self,m): return self.total_load(m)/m.area
    def average_settlement(self,m): return self.average_contact_pressure(m)/m.subgrade_modulus
    def concrete_volume(self,m): return m.area*m.thickness
