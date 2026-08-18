from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class SoilMaterial: material_id:str; name:str; unit_weight:float; cohesion:float; friction_angle_deg:float; elastic_modulus:float
@dataclass(frozen=True,slots=True)
class SoilLayer:
    layer_id:str; top_depth:float; bottom_depth:float; material:SoilMaterial
    @property
    def thickness(self): return self.bottom_depth-self.top_depth
class SoilProfile:
    def __init__(self,profile_id,layers): self.profile_id=profile_id; self.layers=tuple(sorted(layers,key=lambda x:x.top_depth))
    @property
    def total_depth(self): return self.layers[-1].bottom_depth
    def layer_at(self,depth):
        for layer in self.layers:
            if layer.top_depth<=depth<layer.bottom_depth: return layer
        return self.layers[-1]
