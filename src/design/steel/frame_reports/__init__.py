from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class SteelFrameReport:
    markdown:str

class SteelFrameReportEngine:
    def build(self,frame,dashboard,optimization,advice):
        lines=[
            f"# Complete Steel Frame Report — {frame.frame_id}",
            "",
            f"- Nodes: {len(frame.nodes)}",
            f"- Members: {dashboard.total_members}",
            f"- Passed: {dashboard.passed_members}",
            f"- Failed: {dashboard.failed_members}",
            f"- Maximum unity: {dashboard.maximum_unity:.4f}",
            f"- Optimized members: {optimization.optimized_members}",
            f"- Average weight reduction: {optimization.average_weight_reduction_percent:.2f}%",
            "",
            "## AI Advisor",
            advice.summary,
        ]
        for w in advice.warnings: lines.append(f"- Warning: {w}")
        for r in advice.recommendations: lines.append(f"- Recommendation: {r}")
        if dashboard.critical_members:
            lines += ["","## Critical Members"]
            for c in dashboard.critical_members:
                lines.append(f"- {c.member_id} ({c.member_type}): unity={c.unity_ratio:.4f}, governing={c.governing_check}")
        return SteelFrameReport("\n".join(lines)+"\n")
