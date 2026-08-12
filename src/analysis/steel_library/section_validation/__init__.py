from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ValidationResult: valid:bool; warnings:tuple
class SectionValidationEngine:
    def validate(self,s):
        w=[]
        if s.area_mm2<=0:w.append("Area must be positive")
        if s.mass_kg_m<=0:w.append("Mass must be positive")
        if s.ix_mm4<=0 or s.iy_mm4<=0:w.append("Inertia must be positive")
        return ValidationResult(not w,tuple(w))
