from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ConstructabilityScore:
    access:float; repetition:float; field_work:float; tolerance:float; score:float
class ConnectionConstructabilityEngine:
    def score(self,access,repetition,field_work,tolerance):
        value=.3*access+.3*repetition+.2*(1-field_work)+.2*tolerance
        return ConstructabilityScore(access,repetition,field_work,tolerance,value)
