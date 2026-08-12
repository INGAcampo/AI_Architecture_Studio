from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class FemNode: node_id:str; coordinates:tuple
@dataclass(frozen=True,slots=True)
class FemElement: element_id:str; node_ids:tuple; material_id:str
@dataclass(frozen=True,slots=True)
class FemAnalysisResult: displacements:tuple; reactions:tuple; converged:bool
