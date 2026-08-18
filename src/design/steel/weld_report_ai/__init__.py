from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class WeldReport: markdown:str
@dataclass(frozen=True,slots=True)
class WeldAdvice: message:str; recommendations:tuple
class WeldReportAI:
    def build(self,results,opts=()):
        mx=max((r.unity_ratio for r in results),default=0); ok=all(r.passed for r in results)
        lines=["# Weld Connection Design Report","",f"- Welds: {len(results)}",f"- Maximum unity: {mx:.4f}",f"- Status: {'PASS' if ok else 'FAIL'}",""]
        lines += [f"- {r.segment_id}: unity={r.unity_ratio:.4f}, governing={r.governing_check}, status={'PASS' if r.passed else 'FAIL'}" for r in results]
        return WeldReport("\n".join(lines)+"\n")
    def advise(self,results,opts=()):
        ok=all(r.passed for r in results); n=sum(1 for o in opts if o.weld_metal_reduction_percent>0)
        return WeldAdvice("La conexión soldada cumple." if ok else "La conexión soldada no cumple.",(() if not n else (f"Optimizar {n} soldaduras.",)))
