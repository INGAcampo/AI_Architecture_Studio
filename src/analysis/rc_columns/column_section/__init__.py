from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ColumnSection:
    width:float; depth:float
    def area(self): return self.width*self.depth
    def inertia_x(self): return self.width*self.depth**3/12
    def inertia_y(self): return self.depth*self.width**3/12
