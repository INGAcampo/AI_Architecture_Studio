"""Coordinated shallow-foundation calculation engine and governing-case selection."""
from __future__ import annotations
from .models import FoundationInput, CombinationResult, CalculationPackage
from .validation import FoundationCalculationValidator
from .combinations import LoadCombinationEngine
from .bearing import BearingPressureEngine
from .demands import StructuralDemandEngine
from .settlement import SettlementEngine

class FoundationCalculationEngine:
    """Validate inputs, execute every combination and assemble transparent QA evidence."""
    def calculate(self, data: FoundationInput) -> CalculationPackage:
        """Validate and solve all combinations, select governing cases and record QA."""
        issues=FoundationCalculationValidator().validate(data)
        if issues:
            raise ValueError("invalid_input:" + ",".join(issues))

        results=[]
        for combo in data.combinations:
            resultant=LoadCombinationEngine().combine(data.load_cases,combo)
            bearing=BearingPressureEngine().calculate(data,resultant)
            demands=StructuralDemandEngine().calculate(data,resultant,bearing)
            settlement=SettlementEngine().immediate(data,bearing)
            results.append(CombinationResult(combo.name,resultant,bearing,demands,settlement))

        governing={
            "q_max":max(results,key=lambda r:r.bearing.q_max_kpa).combination,
            "punching":max(results,key=lambda r:r.demands.punching_shear_kn).combination,
            "moment_x":max(results,key=lambda r:r.demands.moment_x_knm).combination,
            "moment_y":max(results,key=lambda r:r.demands.moment_y_knm).combination,
        }
        qa={
            "all_allowable_ok":all(r.bearing.allowable_ok for r in results),
            "all_kern_ok":all(r.bearing.kern_ok for r in results),
            "combination_count":len(results),
            "normative_capacity_checks":"NOT_INCLUDED_USE_AEKS_CODE_PACK",
            "human_review_required":True,
        }
        return CalculationPackage(results,governing,qa)
