from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class DynamicReport: markdown:str
class DynamicReportEngine:
    def build(self,r,base_shear,drift):
        lines=["# Modal Seismic Dynamic Analysis Report","",f"- Converged: {r.converged}",f"- Modes: {len(r.modes)}",f"- Base shear: {base_shear:.4f}",f"- Maximum drift ratio: {drift:.6f}"]
        return DynamicReport("\n".join(lines)+"\n")
