"""Human-review-oriented JSON reporting for foundation calculation packages."""
from __future__ import annotations
import json
from pathlib import Path
from .models import FoundationInput, CalculationPackage

class CalculationReportWriter:
    """Persist inputs, results and professional-use limitations in one technical file."""
    def write_json(self, data: FoundationInput, package: CalculationPackage, path: Path) -> Path:
        """Write inputs, results and professional limitations into one technical file."""
        path.parent.mkdir(parents=True,exist_ok=True)
        payload={
            "title":"AIAS Shallow Foundation Calculation Package",
            "inputs":{
                "width_m":data.width_m,"length_m":data.length_m,"thickness_m":data.thickness_m,
                "allowable_bearing_pressure_kpa":data.allowable_bearing_pressure_kpa,
                "concrete_strength_mpa":data.concrete_strength_mpa,
                "steel_yield_strength_mpa":data.steel_yield_strength_mpa,
            },
            "results":package.to_dict(),
            "limitations":[
                "Generic demand engine; jurisdiction-specific resistance checks require an AEKS code pack.",
                "Professional engineering review is mandatory before regulated use."
            ]
        }
        path.write_text(json.dumps(payload,indent=2),encoding="utf-8")
        return path
