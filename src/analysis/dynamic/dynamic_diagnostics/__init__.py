from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class DynamicDiagnosticResult: warnings:tuple
class DynamicDiagnosticsEngine:
    def inspect(self,frequencies,mass_ratio,drift):
        w=[]
        if any(f<=0 for f in frequencies):w.append("Non-positive natural frequency")
        if mass_ratio<.9:w.append("Insufficient modal mass participation")
        if drift>.02:w.append("Seismic drift limit exceeded")
        return DynamicDiagnosticResult(tuple(w))
