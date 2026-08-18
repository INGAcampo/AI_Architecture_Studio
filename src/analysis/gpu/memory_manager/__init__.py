class GPUMemoryManager:
    def __init__(self,total): self.total=total; self.used=0
    def allocate(self,size):
        if self.used+size>self.total: raise MemoryError("GPU out of memory")
        self.used+=size; return size
    def release(self,size): self.used=max(0,self.used-size)
