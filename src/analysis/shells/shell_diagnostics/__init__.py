from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ShellDiagnosticResult: warnings:tuple
class ShellDiagnosticsEngine:
    def inspect(self,converged,fi,bf):
        w=[]
        if not converged:w.append('Shell analysis did not converge')
        if fi>1:w.append('Composite failure criterion exceeded')
        if bf<1:w.append('Shell buckling risk')
        return ShellDiagnosticResult(tuple(w))
