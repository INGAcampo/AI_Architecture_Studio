from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class AnalysisReport: markdown:str
class AnalysisReportEngine:
    def build(self,r,drift):
        return AnalysisReport(f"# Matrix Structural Analysis Report\n\n- Converged: {r.converged}\n- DOF: {len(r.displacements)}\n- Maximum drift ratio: {drift:.6f}\n")
