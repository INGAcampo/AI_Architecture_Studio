from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Catchment:
    catchment_id: str
    area_hectares: float
    runoff_coefficient: float
    rainfall_intensity_mm_h: float

    def __post_init__(self):
        if not self.catchment_id.strip() or self.area_hectares <= 0:
            raise ValueError("Datos inválidos")
        if not 0 <= self.runoff_coefficient <= 1:
            raise ValueError("Coeficiente inválido")
        if self.rainfall_intensity_mm_h < 0:
            raise ValueError("Intensidad inválida")

class StormwaterDrainageEngine:
    def rational_peak_flow(self, catchment):
        return (
            0.00278
            * catchment.runoff_coefficient
            * catchment.rainfall_intensity_mm_h
            * catchment.area_hectares
        )

    def detention_volume(self, inflow_m3_s, outflow_m3_s, duration_s):
        if duration_s < 0:
            raise ValueError("Duración inválida")
        return max(inflow_m3_s - outflow_m3_s, 0.0) * duration_s
