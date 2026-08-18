class CPUGPUScheduler:
    def choose(self,size,gpu_available=True,threshold=1000): return "gpu" if gpu_available and size>=threshold else "cpu"
