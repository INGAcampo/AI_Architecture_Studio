from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class BraceSlendernessResult:
    effective_length: float
    radius_of_gyration: float
    slenderness: float
    acceptable: bool

class BraceSlendernessEngine:
    def calculate(self, brace, profile, limit=200.0):
        effective=brace.length*brace.effective_length_factor
        radius=min(profile.rx,profile.ry)
        slenderness=effective/max(radius,1e-12)
        return BraceSlendernessResult(effective,radius,slenderness,slenderness<=limit)
