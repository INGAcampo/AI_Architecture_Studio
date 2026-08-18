"""Immutable paper-space contracts for interoperable engineering drawings."""
from __future__ import annotations
from dataclasses import asdict,dataclass,field

@dataclass(frozen=True,slots=True)
class Layer:
    """Define a named drawing layer with portable line presentation."""
    name:str;color:str="#000000";lineweight_mm:float=.25;linetype:str="CONTINUOUS";printable:bool=True
@dataclass(frozen=True,slots=True)
class Line:
    """Represent a paper-space line in millimetres."""
    entity_id:str;layer:str;x1:float;y1:float;x2:float;y2:float
@dataclass(frozen=True,slots=True)
class Text:
    """Represent plain portable drawing text without executable markup."""
    entity_id:str;layer:str;x:float;y:float;value:str;height_mm:float=2.5;rotation_deg:float=0.0
@dataclass(frozen=True,slots=True)
class Dimension:
    """Represent a linear dimension with explicit displayed engineering value."""
    entity_id:str;layer:str;x1:float;y1:float;x2:float;y2:float;offset_mm:float;value:float;unit:str="mm"
@dataclass(frozen=True,slots=True)
class View:
    """Declare a model-to-paper viewport scale and clipping rectangle."""
    view_id:str;name:str;scale_denominator:float;x_mm:float;y_mm:float;width_mm:float;height_mm:float;source_ref:str
@dataclass(frozen=True,slots=True)
class Sheet:
    """Define one paper sheet, title-block identity and revision."""
    sheet_id:str;number:str;title:str;width_mm:float;height_mm:float;revision:str;project_id:str;author:str;checker:str;status:str="FOR_REVIEW"
@dataclass(frozen=True,slots=True)
class Drawing:
    """Aggregate one traceable sheet, views, layers and ordered entities."""
    drawing_id:str;version:str;sheet:Sheet;layers:tuple[Layer,...];views:tuple[View,...];entities:tuple[object,...];provenance:dict=field(default_factory=dict);professional_review_required:bool=True
    def to_dict(self)->dict:
        """Serialize the complete drawing into a canonical interchange record."""
        return asdict(self)
