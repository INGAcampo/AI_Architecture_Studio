from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class Diagnostics: warnings:tuple
class FemDiagnostics:
 def inspect(self,K,q): return Diagnostics(tuple(['Poor mesh quality'] if q<.2 else []))
