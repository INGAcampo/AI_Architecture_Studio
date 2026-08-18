from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class WallQuantities:
    gross_area: float
    opening_area: float
    net_area: float
    gross_volume: float
    net_volume: float
    length: float
    height: float
    thickness: float

class WallQuantityEngine:
    def calculate(self, wall, openings=()):
        length = wall.profile.length
        height = wall.profile.height
        thickness = wall.wall_type.structure.total_thickness
        gross_area = length * height
        opening_area = sum(opening.width * opening.height for opening in openings)
        net_area = max(0.0, gross_area - opening_area)
        return WallQuantities(
            gross_area=gross_area,
            opening_area=opening_area,
            net_area=net_area,
            gross_volume=gross_area * thickness,
            net_volume=net_area * thickness,
            length=length,
            height=height,
            thickness=thickness,
        )
