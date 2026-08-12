class CPUGPUContactScheduler:
    def choose(self,count,gpu_available=True,threshold=5000): return "gpu" if gpu_available and count>=threshold else "cpu"
