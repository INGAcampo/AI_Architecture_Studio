from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class BlockShearResult:
    nominal_capacity:float; design_capacity:float; ratio:float; passed:bool
class BlockShearEngine:
    def calculate(self,agv,anv,ant,fy,fu,demand,phi=.75):
        rn=min(.6*fy*agv+fu*ant,.6*fu*anv+fy*ant)
        cap=phi*rn; ratio=demand/max(cap,1e-12)
        return BlockShearResult(rn,cap,ratio,ratio<=1)
