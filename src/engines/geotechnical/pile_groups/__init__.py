from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class PileGroup: group_id:str; pile_count:int; single_pile_capacity:float; efficiency:float; stiffness_per_pile:float
class PileGroupAnalysis:
    def group_capacity(self,g): return g.pile_count*g.single_pile_capacity*g.efficiency
    def settlement(self,g,load): return load/(g.pile_count*g.stiffness_per_pile*g.efficiency)
    def distribute_load(self,g,load): return tuple(load/g.pile_count for _ in range(g.pile_count))
