from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class Report: markdown:str
class TransientReportEngine:
    def build(self,result,peak_u,peak_v,energy_error,backend):
        return Report(f"# Implicit & Explicit Transient Dynamics Report\n\n- Method: {result.method}\n- Converged: {result.converged}\n- Steps: {len(result.steps)}\n- Peak displacement: {peak_u:.6f}\n- Peak velocity: {peak_v:.6f}\n- Energy error: {energy_error:.6f}\n- Backend: {backend}\n")
