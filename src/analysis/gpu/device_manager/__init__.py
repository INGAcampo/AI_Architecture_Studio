class GPUDeviceManager:
    def __init__(self,devices=()): self.devices=tuple(devices)
    def best(self): return max(self.devices,key=lambda d:(d.compute_units,d.memory_bytes)) if self.devices else None
