from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ConnectionReport:
    markdown:str
class ConnectionReportEngine:
    def build(self,connection,result,advice):
        lines=[f"# Steel Connection Report — {connection.connection_id}","",f"- Family: {connection.family.value}",f"- Method: {connection.method.value}",f"- Unity: {result.unity_ratio:.4f}",f"- Governing: {result.governing_check}",f"- Status: {'PASS' if result.passed else 'FAIL'}","","## AI Advisor",advice.summary]
        return ConnectionReport("\n".join(lines)+"\n")
