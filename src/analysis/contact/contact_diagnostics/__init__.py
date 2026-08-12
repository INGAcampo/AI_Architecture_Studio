from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ContactDiagnosticResult: warnings:tuple
class ContactDiagnosticsEngine:
    def inspect(self,converged,penetration,energy_error):
        w=[]
        if not converged:w.append("Contact solution did not converge")
        if penetration>1e-4:w.append("Excessive penetration")
        if energy_error>.05:w.append("High contact energy imbalance")
        return ContactDiagnosticResult(tuple(w))
