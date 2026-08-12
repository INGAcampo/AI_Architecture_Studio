from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ColumnReport: markdown:str
class ColumnReportEngine:
    def build(self,c,r):
        return ColumnReport(f"# Reinforced Concrete Column Design — {c.column_id}\n\n- Axial capacity: {r.axial_capacity:.2f} N\n- Moment capacity X: {r.moment_capacity_x:.2f} N·mm\n- Moment capacity Y: {r.moment_capacity_y:.2f} N·mm\n- Interaction ratio: {r.interaction_ratio:.4f}\n- Slenderness ratio: {r.slenderness_ratio:.4f}\n- Status: {r.status}\n")
