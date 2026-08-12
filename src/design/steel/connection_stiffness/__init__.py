from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ConnectionStiffnessResult:
    initial_stiffness:float; secant_stiffness:float; classification:str
class ConnectionStiffnessEngine:
    def classify(self,moment,rotation,beam_stiffness):
        secant=abs(moment)/max(abs(rotation),1e-12)
        ratio=secant/max(beam_stiffness,1e-12)
        cls="rigid" if ratio>=8 else ("semi_rigid" if ratio>=0.5 else "pinned")
        return ConnectionStiffnessResult(secant,secant,cls)
