from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class MaterialDiagnosticResult:warnings:tuple
class MaterialDiagnosticsEngine:
    def inspect(self,ok,d,ep):
        w=[]
        if not ok:w.append('Constitutive integration did not converge')
        if d>.95:w.append('Severe material damage')
        if ep>.2:w.append('Large plastic strain')
        return MaterialDiagnosticResult(tuple(w))
