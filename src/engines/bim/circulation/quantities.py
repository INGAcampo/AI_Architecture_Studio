from dataclasses import dataclass
@dataclass(frozen=True,slots=True)
class CirculationQuantities:
    rise: float
    run: float
    path_length: float
    floor_area: float
    riser_count: int
    tread_count: int
class CirculationQuantityCalculator:
    def calculate(self,item):
        return CirculationQuantities(item.rise,item.calculated_run,item.path_length,item.width*item.calculated_run,item.riser_count,item.tread_count)
