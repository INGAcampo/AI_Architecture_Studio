"""Minimum cover and thickness checks supplied by the active code pack."""
from __future__ import annotations
from .models import CodePack, DesignInput, CheckResult

class ServiceabilityCheckEngine:
    """Report dimension compliance as demand, capacity and utilization records."""
    def cover(self, data: DesignInput, pack: CodePack) -> CheckResult:
        """Compare supplied cover with the code-pack minimum in millimetres."""
        required=pack.parameters.get("minimum_cover_mm",50.0)
        actual=data.cover_m*1000
        util=required/actual if actual>0 else float("inf")
        return CheckResult("MINIMUM_COVER",required,actual,util,actual>=required,"mm","GEN-RC-COVER-001")

    def thickness(self, data: DesignInput, pack: CodePack) -> CheckResult:
        """Compare supplied thickness with the code-pack minimum in millimetres."""
        required=pack.parameters.get("minimum_thickness_mm",250.0)
        actual=data.thickness_m*1000
        util=required/actual if actual>0 else float("inf")
        return CheckResult("MINIMUM_THICKNESS",required,actual,util,actual>=required,"mm","GEN-RC-THK-001")
