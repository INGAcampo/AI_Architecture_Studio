from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class RCReport: markdown:str
class RCReportEngine:
    def build(self,beam,result):
        return RCReport(f"# Reinforced Concrete Beam Design — {beam.beam_id}\n\n- Required steel area: {result.steel_area:.2f} mm²\n- Design moment: {result.design_moment:.2f} N·mm\n- Shear capacity: {result.shear_capacity:.2f} N\n- Utilization: {result.utilization:.4f}\n- Status: {result.status}\n")
