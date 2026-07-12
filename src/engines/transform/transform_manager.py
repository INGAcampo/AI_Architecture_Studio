"""
AI Architecture Studio
Transform Manager

Foundation 3.5
"""


class TransformManager:

    @staticmethod
    def move_point(point, dx, dy, dz=0.0):
        point.x += dx
        point.y += dy
        point.z += dz

    @staticmethod
    def move_line(line, dx, dy, dz=0.0):
        TransformManager.move_point(
            line.start,
            dx,
            dy,
            dz
        )

        TransformManager.move_point(
            line.end,
            dx,
            dy,
            dz
        )

    @staticmethod
    def move_polyline(polyline, dx, dy, dz=0.0):
        for point in polyline.points:
            TransformManager.move_point(
                point,
                dx,
                dy,
                dz
            )

    @staticmethod
    def move_circle(circle, dx, dy, dz=0.0):
        TransformManager.move_point(
            circle.center,
            dx,
            dy,
            dz
        )

    @staticmethod
    def move_element(element, dx, dy, dz=0.0):
        geometry = getattr(
            element,
            "geometry",
            None
        )

        if (
            geometry is not None
            and geometry.__class__.__name__ == "Line"
        ):
            TransformManager.move_line(
                geometry,
                dx,
                dy,
                dz
            )
            return True

        element_type = element.__class__.__name__

        if element_type == "CadPolyline":
            TransformManager.move_polyline(
                element,
                dx,
                dy,
                dz
            )
            return True

        if element_type == "CadRectangle":
            TransformManager.move_polyline(
                element.polyline,
                dx,
                dy,
                dz
            )
            return True

        if element_type == "CadCircle":
            TransformManager.move_circle(
                element,
                dx,
                dy,
                dz
            )
            return True

        return False