"""Technical JSON report generation with explicit normative-use limitations."""
from pathlib import Path
import json
from .models import DesignInput,CodeCheckPackage

class CodeCheckReportWriter:
    """Persist code provenance, inputs, results and regulated-use notices together."""
    def write(self,data:DesignInput,result:CodeCheckPackage,path:Path)->Path:
        """Persist code provenance, inputs, results and regulated-use notices."""
        path.parent.mkdir(parents=True,exist_ok=True)
        payload={
            "title":"AIAS Foundation Code Check Package",
            "code_pack":result.code_pack,
            "input":{
                "width_m":data.width_m,"length_m":data.length_m,
                "thickness_m":data.thickness_m,"effective_depth_m":data.effective_depth_m,
                "concrete_strength_mpa":data.concrete_strength_mpa,
                "steel_yield_strength_mpa":data.steel_yield_strength_mpa
            },
            "result":result.to_dict(),
            "legal_notice":[
                "REFERENCE_ONLY packs are not legal design standards.",
                "Regulated use requires a VERIFIED_OFFICIAL AEKS code pack and professional review."
            ]
        }
        path.write_text(json.dumps(payload,indent=2),encoding="utf-8")
        return path
