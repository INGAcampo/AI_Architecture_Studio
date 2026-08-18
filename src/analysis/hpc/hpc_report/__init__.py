from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class Report: markdown:str
class HPCReportEngine:
    def build(self,w,it,res,speed,eff):
        return Report(f"# Parallel FEM Solver Report\n\n- Workers: {w}\n- Iterations: {it}\n- Residual: {res:.6e}\n- Speedup: {speed:.4f}\n- Efficiency: {eff:.4f}\n")
