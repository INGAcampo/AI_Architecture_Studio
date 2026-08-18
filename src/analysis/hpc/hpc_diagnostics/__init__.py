from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class Diagnostic: warnings:tuple
class HPCDiagnosticsEngine:
    def inspect(self,converged,efficiency,memory):
        w=[]
        if not converged:w.append("Iterative solver did not converge")
        if efficiency<.5:w.append("Low parallel efficiency")
        if memory>.9:w.append("High memory pressure")
        return Diagnostic(tuple(w))
