class GPUBenchmarkEngine:
    def speedup(self,cpu,gpu): return cpu/max(gpu,1e-12)
