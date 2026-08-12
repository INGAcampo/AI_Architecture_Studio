from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class GPUDiagnosticResult: warnings:tuple
class GPUDiagnosticsEngine:
    def inspect(self,available,memory_ratio,converged):
        w=[]
        if not available:w.append("No GPU device available")
        if memory_ratio>.9:w.append("High GPU memory pressure")
        if not converged:w.append("GPU solver did not converge")
        return GPUDiagnosticResult(tuple(w))
