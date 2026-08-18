from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class CirculationValidationResult:
    valid: bool
    errors: tuple[str,...]=()
class CirculationValidator:
    def validate(self,item):
        errors=[]
        if item.kind.value.endswith("stair"):
            if not 0.10 <= item.actual_riser_height <= 0.22: errors.append("Contrahuella fuera de rango")
            if item.tread_depth < 0.22: errors.append("Huella insuficiente")
        if item.kind.value=="ramp" and item.slope > 0.12: errors.append("Pendiente de rampa excesiva")
        return CirculationValidationResult(not errors,tuple(errors))
