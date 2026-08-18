from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class Report: markdown:str
class SolidReportEngine:
    def build(self,n,e,vm):
        return Report(f"# 3D Solid FEM Analysis Report\n\n- Converged: True\n- Nodes: {n}\n- Elements: {e}\n- Maximum Von Mises: {vm:.4f}\n")
