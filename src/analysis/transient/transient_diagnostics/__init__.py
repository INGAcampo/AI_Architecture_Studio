from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class Diagnostic: warnings:tuple
class TransientDiagnosticsEngine:
    def inspect(self,converged,energy_error,stable):
        w=[]
        if not converged:w.append("Transient analysis did not converge")
        if energy_error>.05:w.append("Energy balance error exceeded")
        if not stable:w.append("Explicit time step is unstable")
        return Diagnostic(tuple(w))
