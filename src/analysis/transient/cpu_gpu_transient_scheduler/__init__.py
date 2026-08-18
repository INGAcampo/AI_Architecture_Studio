class CPUGPUTransientScheduler:
    def choose(self,dofs,steps,gpu_available=True,threshold=100000):
        return "gpu" if gpu_available and dofs*steps>=threshold else "cpu"
