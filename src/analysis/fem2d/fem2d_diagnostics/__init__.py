from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class Fem2DDiagnosticResult: warnings:tuple
class Fem2DDiagnosticsEngine:
    def inspect(self,q,e):
        w=[]
        if q<.2:w.append('Poor element quality')
        if e>.1:w.append('High discretization error')
        return Fem2DDiagnosticResult(tuple(w))