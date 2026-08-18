from dataclasses import dataclass
from analysis.gpu.gpu_domain import GPUDevice
from analysis.gpu.device_manager import GPUDeviceManager
from analysis.gpu.gpu_cg import GPUConjugateGradientSolver
from analysis.gpu.gpu_benchmark import GPUBenchmarkEngine
from analysis.gpu.gpu_diagnostics import GPUDiagnosticsEngine
from analysis.gpu.gpu_ai_optimizer import GPUAIOptimizer
from analysis.gpu.gpu_result_pipeline import GPUResultPipeline
@dataclass(frozen=True,slots=True)
class GPUWorkflowResult:
    solution:tuple;run:object;device:object;diagnostics:object;optimization:object;speedup:float;normalized_solution:tuple
class GPUVerticalSlice:
    def run(self,A,b,size=5000):
        d=GPUDevice("GPU0","AIAS Simulated GPU","simulated",8_000_000_000,32)
        dev=GPUDeviceManager((d,)).best();x,run=GPUConjugateGradientSolver().solve(A,b)
        diag=GPUDiagnosticsEngine().inspect(True,.4,run.converged)
        return GPUWorkflowResult(x,run,dev,diag,GPUAIOptimizer().recommend(size,d.memory_bytes),GPUBenchmarkEngine().speedup(3,1),GPUResultPipeline().normalize(x))
