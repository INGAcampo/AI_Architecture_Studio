from dataclasses import dataclass,asdict
@dataclass
class ProjectSettings:
    units:str="metric"; precision:int=3; grid_spacing:float=1.0
    snap_enabled:bool=True; ortho_enabled:bool=False
    autosave_enabled:bool=True; autosave_interval_seconds:int=300
    def to_dict(self): return asdict(self)
    @classmethod
    def from_dict(cls,data):
        allowed=cls.__dataclass_fields__.keys(); return cls(**{k:v for k,v in data.items() if k in allowed})
