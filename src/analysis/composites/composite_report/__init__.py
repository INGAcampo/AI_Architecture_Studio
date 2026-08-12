from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class CompositeReport: markdown:str
class CompositeReportEngine:
    def build(self,result,delamination_index):
        return CompositeReport(f"# Progressive Composite Damage & Delamination Report\n\n- Converged: {result.converged}\n- Iterations: {result.iterations}\n- Failure index: {result.failure_index:.4f}\n- Fiber damage: {result.state.fiber_damage:.6f}\n- Matrix damage: {result.state.matrix_damage:.6f}\n- Delamination index: {delamination_index:.4f}\n")
