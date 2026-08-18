"""Parameter-driven flexural reinforcement sizing for rectangular foundations."""
from __future__ import annotations
from .models import CodePack, DesignInput, ReinforcementResult

class FlexureDesignEngine:
    """Compute required steel and enforce code-pack minimum reinforcement ratios."""
    def _required_steel(self, moment_knm: float, width_m: float, data: DesignInput, pack: CodePack) -> float:
        phi=pack.parameters["phi_flexure"]
        fs=pack.parameters["steel_stress_limit_factor"]*data.steel_yield_strength_mpa
        lever_arm_m=0.9*data.effective_depth_m
        if phi<=0 or fs<=0 or lever_arm_m<=0:
            raise ValueError("invalid_flexure_parameters")
        return abs(moment_knm)*1_000_000/(phi*fs*lever_arm_m*1000)

    def design(self, data: DesignInput, pack: CodePack) -> ReinforcementResult:
        """Calculate required and minimum reinforcement for both footing directions."""
        req_x=self._required_steel(data.factored_moment_x_knm,data.length_m,data,pack)
        req_y=self._required_steel(data.factored_moment_y_knm,data.width_m,data,pack)
        gross_x=data.length_m*1000*data.thickness_m*1000
        gross_y=data.width_m*1000*data.thickness_m*1000
        min_x=pack.parameters["min_reinforcement_ratio"]*gross_x
        min_y=pack.parameters["min_reinforcement_ratio"]*gross_y
        gov_x=max(req_x,min_x)
        gov_y=max(req_y,min_y)
        return ReinforcementResult(req_x,req_y,min_x,min_y,gov_x,gov_y,None,None)
