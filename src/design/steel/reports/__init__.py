from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class SteelCalculationReport:
    title: str
    markdown: str

class SteelReportEngine:
    def build(self, b, p, m, r, opt=None):
        status = "PASS" if r.passed else "FAIL"
        text = (
            f"# Steel Beam Design — {b.member_id}\n\n"
            f"- Profile: {p.designation}\n"
            f"- Material: {m.name}\n"
            f"- Unity: {r.unity_ratio:.4f}\n"
            f"- Governing: {r.governing_check}\n"
            f"- Status: {status}\n"
        )
        if opt is not None:
            text += (
                f"- Recommended: {opt.recommended_profile_id}\n"
                f"- Weight reduction: {opt.weight_reduction_percent:.2f}%\n"
            )
        return SteelCalculationReport(f"Steel Beam {b.member_id}", text)
