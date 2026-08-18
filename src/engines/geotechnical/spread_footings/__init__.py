from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class SpreadFooting:
    footing_id:str; width:float; length:float; vertical_load:float; allowable_bearing_pressure:float
    @property
    def area(self): return self.width*self.length
class SpreadFootingDesign:
    def average_pressure(self,f): return f.vertical_load/f.area
    def bearing_ok(self,f): return self.average_pressure(f)<=f.allowable_bearing_pressure
