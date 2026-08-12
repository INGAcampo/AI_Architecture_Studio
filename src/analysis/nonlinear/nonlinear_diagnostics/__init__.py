from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class NonlinearDiagnosticResult: warnings:tuple
class NonlinearDiagnosticsEngine:
 def inspect(self,r,limit=.01):
  w=[]
  if not r.converged:w.append('Nonlinear analysis did not converge')
  if any(abs(s.residual)>limit for s in r.steps):w.append('Residual limit exceeded')
  return NonlinearDiagnosticResult(tuple(w))
