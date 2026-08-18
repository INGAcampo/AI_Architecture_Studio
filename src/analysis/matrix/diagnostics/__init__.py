from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class DiagnosticResult: warnings:tuple
class StructuralDiagnostics:
    def inspect(self,K):
        return DiagnosticResult(tuple(["Zero stiffness detected"] if any(abs(K[i][i])<1e-12 for i in range(len(K))) else []))
