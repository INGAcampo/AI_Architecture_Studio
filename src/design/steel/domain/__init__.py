from dataclasses import dataclass,field
from enum import Enum
class SteelProfileFamily(str,Enum): W='W';HSS='HSS';IPE='IPE';HEA='HEA';HEB='HEB';C='C';L='L';UPN='UPN'
@dataclass(frozen=True,slots=True)
class SteelProfile:
    profile_id:str;designation:str;family:SteelProfileFamily;area:float;weight_per_length:float;ix:float;iy:float;sx:float;sy:float;zx:float;zy:float;rx:float;ry:float;j:float=0.;cw:float=0.
    def __post_init__(self):
        if not self.profile_id.strip() or not self.designation.strip(): raise ValueError('Identificación obligatoria')
        if min(self.area,self.ix,self.iy,self.sx,self.sy,self.zx,self.zy,self.rx,self.ry)<=0: raise ValueError('Propiedades inválidas')
@dataclass(frozen=True,slots=True)
class SteelMaterial: material_id:str;name:str;fy:float;fu:float;elastic_modulus:float;density:float;standard:str='CUSTOM'
@dataclass(frozen=True,slots=True)
class SteelMemberDemand: axial:float=0.;shear:float=0.;moment:float=0.;torsion:float=0.
@dataclass(frozen=True,slots=True)
class SteelBeam: member_id:str;profile_id:str;material_id:str;length:float;unbraced_length:float;demand:SteelMemberDemand=SteelMemberDemand();metadata:dict=field(default_factory=dict)
@dataclass(frozen=True,slots=True)
class SteelDesignResult: member_id:str;axial_ratio:float;shear_ratio:float;flexural_ratio:float;interaction_ratio:float;unity_ratio:float;passed:bool;governing_check:str
