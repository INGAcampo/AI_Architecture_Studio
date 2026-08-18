from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class SeatAngleResult:
    bearing_ratio:float; bending_ratio:float; weld_ratio:float; unity_ratio:float; passed:bool
class SeatAngleEngine:
    def design(self,demand,bearing_cap,bending_cap,weld_cap):
        rs=(demand/bearing_cap,demand/bending_cap,demand/weld_cap); u=max(rs)
        return SeatAngleResult(*rs,u,u<=1)
