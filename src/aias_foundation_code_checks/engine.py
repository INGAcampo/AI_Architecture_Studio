"""Coordinated foundation reinforcement and demand-capacity checking pipeline."""
from __future__ import annotations
from dataclasses import asdict
from .models import CodePack, DesignInput, CodeCheckPackage
from .validation import CodeCheckValidator
from .flexure import FlexureDesignEngine
from .shear import ShearCheckEngine
from .serviceability import ServiceabilityCheckEngine

class FoundationCodeCheckEngine:
    """Validate inputs and pack, execute checks, and preserve legal-review boundaries."""
    def check(self, data: DesignInput, pack: CodePack) -> CodeCheckPackage:
        """Validate, design reinforcement, execute checks and attach legal QA evidence."""
        validator=CodeCheckValidator()
        issues=validator.validate_pack(pack)+validator.validate_input(data)
        if issues:
            raise ValueError("invalid_code_check:" + ",".join(issues))

        reinforcement=FlexureDesignEngine().design(data,pack)
        shear=ShearCheckEngine()
        service=ServiceabilityCheckEngine()
        checks=[
            shear.one_way(data.factored_one_way_shear_x_kn,data.length_m,data,pack,"X"),
            shear.one_way(data.factored_one_way_shear_y_kn,data.width_m,data,pack,"Y"),
            shear.punching(data.factored_punching_shear_kn,data,pack),
            service.cover(data,pack),
            service.thickness(data,pack),
        ]
        qa={
            "all_passed":all(c.passed for c in checks),
            "legal_status":pack.legal_status,
            "verified_official_required_for_regulated_use":pack.legal_status!="VERIFIED_OFFICIAL",
            "human_review_required":True,
            "equation_traceability":True,
        }
        return CodeCheckPackage(asdict(pack),checks,reinforcement,qa)
