from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class SteelColumnReport:
    title:str
    markdown:str

class SteelColumnReportEngine:
    def build(self,column,profile,material,result,optimization=None):
        lines=[
            f"# Steel Column Design — {column.member_id}",
            "",
            f"- Profile: {profile.designation}",
            f"- Material: {material.name}",
            f"- Length: {column.length:.3f} m",
            f"- Slenderness major: {result.slenderness_major:.3f}",
            f"- Slenderness minor: {result.slenderness_minor:.3f}",
            f"- Critical axis: {result.critical_axis.value}",
            f"- Compression capacity: {result.compression_capacity:.3f} N",
            f"- Axial ratio: {result.axial_ratio:.4f}",
            f"- Major bending ratio: {result.major_bending_ratio:.4f}",
            f"- Minor bending ratio: {result.minor_bending_ratio:.4f}",
            f"- Interaction ratio: {result.interaction_ratio:.4f}",
            f"- Unity: {result.unity_ratio:.4f}",
            f"- Status: {'PASS' if result.passed else 'FAIL'}",
        ]
        if optimization:
            lines += ["", "## Optimization", f"- Recommended: {optimization.recommended_profile_id}", f"- Weight reduction: {optimization.weight_reduction_percent:.2f}%"]
        return SteelColumnReport(f"Steel Column {column.member_id}","\n".join(lines)+"\n")
