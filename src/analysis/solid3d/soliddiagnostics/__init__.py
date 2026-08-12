from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class Diagnostic: warnings:tuple
class SolidDiagnosticsEngine:
    def inspect(self,q,e):
        w=[]
        if q<.1:w.append("Poor 3D mesh quality")
        if e>.15:w.append("High discretization error")
        return Diagnostic(tuple(w))
