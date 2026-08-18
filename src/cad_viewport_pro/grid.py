import math

class AdaptiveGrid:
    STEPS = (0.1,0.2,0.5,1,2,5,10,20,50,100,200,500,1000)

    def spacing(self, zoom: float, target_pixels: float = 40.0) -> float:
        target = target_pixels / max(zoom, 1e-9)
        return min(self.STEPS, key=lambda step: abs(math.log10(step / target)))
