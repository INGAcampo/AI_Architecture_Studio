"""Perfil normativo configurable de un proyecto AIAS."""

from dataclasses import dataclass, field, asdict
from typing import Dict, List


@dataclass
class StandardProfile:
    profile_id: str
    name: str
    country: str
    jurisdiction: str = ""
    structural_basis: str = ""
    concrete_code: str = ""
    steel_code: str = ""
    load_code: str = ""
    seismic_code: str = ""
    wind_code: str = ""
    geotechnical_code: str = ""
    fire_code: str = ""
    accessibility_code: str = ""
    quality_code: str = ""
    bim_standard: str = "IFC / ISO 19650"
    editions: Dict[str, str] = field(default_factory=dict)
    notes: str = ""
    enabled_modules: List[str] = field(default_factory=list)
    verified: bool = False

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        allowed = {
            field_name
            for field_name in cls.__dataclass_fields__.keys()
        }
        clean = {
            key: value
            for key, value in dict(data or {}).items()
            if key in allowed
        }
        return cls(**clean)

    def summary(self):
        return {
            "Perfil": self.name,
            "País": self.country,
            "Jurisdicción": self.jurisdiction or "-",
            "Base estructural": self.structural_basis or "-",
            "Concreto": self.concrete_code or "-",
            "Acero": self.steel_code or "-",
            "Cargas": self.load_code or "-",
            "Sismo": self.seismic_code or "-",
            "Viento": self.wind_code or "-",
            "Geotecnia": self.geotechnical_code or "-",
            "Incendio": self.fire_code or "-",
            "Accesibilidad": self.accessibility_code or "-",
            "Calidad": self.quality_code or "-",
            "BIM": self.bim_standard or "-",
            "Verificado": "Sí" if self.verified else "Pendiente",
        }
