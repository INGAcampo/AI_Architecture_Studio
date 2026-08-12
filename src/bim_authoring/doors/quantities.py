from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class DoorQuantities:
    opening_area: float
    panel_area: float
    panel_volume: float
    perimeter: float

class DoorQuantityEngine:
    def calculate(self, door):
        width = door.door_type.width
        height = door.door_type.height
        thickness = door.door_type.panel.thickness
        area = width * height
        return DoorQuantities(
            opening_area=area,
            panel_area=area,
            panel_volume=area * thickness,
            perimeter=2 * (width + height),
        )
