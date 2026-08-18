from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ColumnDiagnosticResult: warnings:tuple
class ColumnDiagnosticsEngine:
    def inspect(self,interaction,slenderness,ratio_ok,seismic_ok):
        w=[]
        if interaction>1:w.append("Column interaction capacity exceeded")
        if slenderness>100:w.append("Column slenderness is high")
        if not ratio_ok:w.append("Longitudinal reinforcement ratio out of bounds")
        if not seismic_ok:w.append("Strong-column weak-beam requirement not met")
        return ColumnDiagnosticResult(tuple(w))
