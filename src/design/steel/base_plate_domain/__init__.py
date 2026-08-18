from dataclasses import dataclass
from enum import Enum

class PlateShape(str,Enum):
    RECTANGULAR="rectangular"
    SQUARE="square"

class AnchorGrade(str,Enum):
    F1554_36="F1554_36"
    F1554_55="F1554_55"
    F1554_105="F1554_105"

@dataclass(frozen=True,slots=True)
class BasePlate:
    plate_id:str
    width:float
    length:float
    thickness:float
    fy:float
    shape:PlateShape=PlateShape.RECTANGULAR

@dataclass(frozen=True,slots=True)
class ColumnFootprint:
    width:float
    depth:float

@dataclass(frozen=True,slots=True)
class BasePlateDemand:
    axial:float
    shear_x:float=0.0
    shear_y:float=0.0
    moment_x:float=0.0
    moment_y:float=0.0

@dataclass(frozen=True,slots=True)
class AnchorRod:
    anchor_id:str
    diameter:float
    grade:AnchorGrade
    fy:float
    fu:float
    x:float
    y:float
