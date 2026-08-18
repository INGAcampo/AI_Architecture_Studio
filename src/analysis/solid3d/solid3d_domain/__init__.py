from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class SolidNode: node_id:str; coordinates:tuple
@dataclass(frozen=True,slots=True)
class SolidElement: element_id:str; node_ids:tuple; material_id:str
