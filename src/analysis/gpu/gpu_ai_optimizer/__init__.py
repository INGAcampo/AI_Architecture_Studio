from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class GPUOptimizationAdvice: backend:str; block_size:int; use_async:bool
class GPUAIOptimizer:
    def recommend(self,size,memory):
        backend="gpu" if size>=1000 and memory>=1_000_000 else "cpu"
        return GPUOptimizationAdvice(backend,256 if backend=="gpu" else 1,backend=="gpu")
