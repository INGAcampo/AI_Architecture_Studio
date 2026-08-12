from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class Fem2DReport: markdown:str
class Fem2DReportEngine:
    def build(self,n,e,s,err,ok): return Fem2DReport(f"# Advanced 2D FEM Analysis Report\n\n- Converged: {ok}\n- Nodes: {n}\n- Elements: {e}\n- Maximum stress: {s:.4f}\n- Maximum error: {err:.6f}\n")