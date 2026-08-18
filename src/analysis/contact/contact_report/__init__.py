from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ContactReport: markdown:str
class ContactReportEngine:
    def build(self,r,mu,backend):
        return ContactReport(f"# Advanced Nonlinear Contact Report\n\n- Converged: {r.converged}\n- Iterations: {r.iterations}\n- Contact points: {len(r.points)}\n- Maximum penetration: {r.maximum_penetration:.6e}\n- Friction coefficient: {mu:.4f}\n- Backend: {backend}\n")
