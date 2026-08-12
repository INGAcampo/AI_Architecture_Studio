from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class WindowQuantities:
    opening_area: float
    glass_area: float
    frame_perimeter: float
    estimated_heat_transfer: float

class WindowQuantityEngine:
    def calculate(self, window, delta_temperature=1.0):
        width = window.window_type.width
        height = window.window_type.height
        opening_area = width * height
        inset = window.window_type.frame.face_width
        glass_width = max(0.0, width - 2 * inset)
        glass_height = max(0.0, height - 2 * inset)
        glass_area = glass_width * glass_height
        return WindowQuantities(
            opening_area=opening_area,
            glass_area=glass_area,
            frame_perimeter=2 * (width + height),
            estimated_heat_transfer=(
                opening_area
                * window.window_type.glass.u_value
                * float(delta_temperature)
            ),
        )
