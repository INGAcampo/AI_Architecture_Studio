from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ContactPoint: slave_id:str; master_id:str; gap:float; normal:tuple; pressure:float; state:str
@dataclass(frozen=True,slots=True)
class ContactResult: points:tuple; converged:bool; iterations:int; maximum_penetration:float
