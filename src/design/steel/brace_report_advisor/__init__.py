from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class BraceReport:
    markdown:str

@dataclass(frozen=True, slots=True)
class BraceAdvice:
    message:str
    critical_members:tuple[str,...]

class BraceReportAdvisor:
    def build_report(self,batch):
        lines=["# Steel Brace System Report","",f"- Members: {len(batch.results)}",f"- Passed: {batch.passed_count}",f"- Failed: {batch.failed_count}",f"- Maximum unity: {batch.maximum_unity:.4f}",""]
        for r in batch.results:
            lines.append(f"- {r.member_id}: unity={r.unity_ratio:.4f}, status={'PASS' if r.passed else 'FAIL'}, governing={r.governing_check}")
        return BraceReport("\n".join(lines)+"\n")
    def advise(self,batch,threshold=0.9):
        critical=tuple(r.member_id for r in batch.results if r.unity_ratio>=threshold)
        message="No hay arriostres críticos." if not critical else f"Arriostres críticos: {', '.join(critical)}."
        return BraceAdvice(message,critical)
