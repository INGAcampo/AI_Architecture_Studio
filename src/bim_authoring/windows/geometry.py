from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class WindowGeometry:
    window_id: str
    frame_vertices: tuple[tuple[float, float, float], ...]
    glass_vertices: tuple[tuple[float, float, float], ...]
    mullions: tuple[tuple[tuple[float, float, float], tuple[float, float, float]], ...]
    width: float
    height: float

class WindowGeometryBuilder:
    def build(self, window):
        width = window.window_type.width
        height = window.window_type.height
        x0 = window.offset
        x1 = x0 + width
        z0 = window.sill_height
        z1 = z0 + height

        frame = (
            (x0, 0, z0),
            (x1, 0, z0),
            (x1, 0, z1),
            (x0, 0, z1),
        )

        inset = window.window_type.frame.face_width
        glass = (
            (x0 + inset, 0, z0 + inset),
            (x1 - inset, 0, z0 + inset),
            (x1 - inset, 0, z1 - inset),
            (x0 + inset, 0, z1 - inset),
        )

        mullions = []
        for index in range(window.window_type.mullion_count_vertical):
            ratio = (index + 1) / (window.window_type.mullion_count_vertical + 1)
            x = x0 + width * ratio
            mullions.append(((x, 0, z0), (x, 0, z1)))
        for index in range(window.window_type.mullion_count_horizontal):
            ratio = (index + 1) / (window.window_type.mullion_count_horizontal + 1)
            z = z0 + height * ratio
            mullions.append(((x0, 0, z), (x1, 0, z)))

        return WindowGeometry(
            window.window_id,
            frame,
            glass,
            tuple(mullions),
            width,
            height,
        )
