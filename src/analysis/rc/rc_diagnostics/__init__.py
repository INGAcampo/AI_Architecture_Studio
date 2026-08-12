from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class RCDiagnosticResult: warnings:tuple
class RCDiagnosticsEngine:
    def inspect(self,utilization,serviceable,ductile):
        w=[]
        if utilization>1:w.append("Flexural capacity exceeded")
        if not serviceable:w.append("Serviceability limits exceeded")
        if not ductile:w.append("Section is not tension controlled")
        return RCDiagnosticResult(tuple(w))
