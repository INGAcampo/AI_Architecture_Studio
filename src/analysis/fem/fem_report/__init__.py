from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class FemReport: markdown:str
class FemReportEngine:
 def build(self,r,n,e,vm): return FemReport(f'# Finite Element Analysis Report\n\n- Converged: {r.converged}\n- Nodes: {n}\n- Elements: {e}\n- Maximum Von Mises: {vm:.4f}\n')
