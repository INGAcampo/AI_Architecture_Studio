from dataclasses import dataclass

@dataclass(frozen=True,slots=True)
class GroutLayerResult:
    pressure:float
    compressive_capacity:float
    ratio:float
    passed:bool

class GroutLayerEngine:
    def calculate(self,load,area,grout_strength,phi=.65):
        pressure=load/max(area,1e-12)
        cap=phi*.85*grout_strength
        ratio=pressure/max(cap,1e-12)
        return GroutLayerResult(pressure,cap,ratio,ratio<=1)
