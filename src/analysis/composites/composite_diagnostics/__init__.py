from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class CompositeDiagnosticResult: warnings:tuple
class CompositeDiagnosticsEngine:
    def inspect(self,converged,maximum_damage,delamination_index):
        w=[]
        if not converged:w.append('Progressive damage loop did not converge')
        if maximum_damage>.95:w.append('Severe ply damage')
        if delamination_index>1.0:w.append('Delamination criterion exceeded')
        return CompositeDiagnosticResult(tuple(w))
