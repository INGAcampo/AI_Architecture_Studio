"""Elastic immediate-settlement estimate with explicit data-availability status."""
from __future__ import annotations
from .models import FoundationInput, BearingResult, SettlementResult

class SettlementEngine:
    """Estimate rectangular-footing settlement when a positive soil modulus is supplied."""
    def immediate(self, data: FoundationInput, bearing: BearingResult) -> SettlementResult:
        """Return elastic immediate settlement or an explicit unavailable result."""
        if data.soil_modulus_mpa is None or data.soil_modulus_mpa <= 0:
            return SettlementResult(None,"ELASTIC_RECTANGULAR_ESTIMATE",False)
        es_kpa=data.soil_modulus_mpa*1000.0
        characteristic=min(data.width_m,data.length_m)
        influence=1.0
        s_m=bearing.q_avg_kpa*characteristic*(1-data.poisson_ratio**2)*influence/es_kpa
        return SettlementResult(s_m*1000.0,"ELASTIC_RECTANGULAR_ESTIMATE",True)
