from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class ConnectionCostResult:
    steel_cost:float; bolt_cost:float; weld_cost:float; labor_cost:float; total_cost:float
class ConnectionCostEngine:
    def estimate(self,steel_mass,steel_rate,bolt_count,bolt_rate,weld_length,weld_rate,labor_hours,labor_rate):
        vals=(steel_mass*steel_rate,bolt_count*bolt_rate,weld_length*weld_rate,labor_hours*labor_rate)
        return ConnectionCostResult(*vals,sum(vals))
