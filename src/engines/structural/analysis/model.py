from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class AnalysisNode:
    node_id:str; x:float; y:float; z:float
    def __post_init__(self):
        if not self.node_id.strip(): raise ValueError("node_id obligatorio")
@dataclass(frozen=True,slots=True)
class BarElement:
    element_id:str; start_node_id:str; end_node_id:str; area:float; elastic_modulus:float
    def __post_init__(self):
        if not self.element_id.strip() or self.area<=0 or self.elastic_modulus<=0: raise ValueError("Datos inválidos")
