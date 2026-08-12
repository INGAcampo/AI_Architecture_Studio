from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class PlateLimitStateResult:
    gross_yield_capacity:float; net_rupture_capacity:float; design_capacity:float; governing:str
class PlateLimitStateEngine:
    def calculate(self,width,thickness,holes,fy,fu,phi_y=.9,phi_u=.75):
        ag=width*thickness
        an=max(width-sum(holes),0)*thickness
        y=phi_y*fy*ag; r=phi_u*fu*an
        return PlateLimitStateResult(y,r,min(y,r),"gross_yield" if y<=r else "net_rupture")
