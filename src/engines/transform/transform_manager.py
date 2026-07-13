"""
AI Architecture Studio
Transform Manager

Foundation 3.5
"""

import math


class TransformManager:

    @staticmethod
    def move_point(point, dx, dy, dz=0.0):
        point.x += dx
        point.y += dy
        point.z += dz

    @staticmethod
    def rotate_point(point, angle, cx=0.0, cy=0.0, cz=0.0):
        dx = point.x - cx
        dy = point.y - cy
        dz = point.z - cz

        cos_a = math.cos(angle)
        sin_a = math.sin(angle)

        point.x = cx + dx * cos_a - dy * sin_a
        point.y = cy + dx * sin_a + dy * cos_a
        point.z = cz + dz

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
    def rotate_line(line, angle, cx=0.0, cy=0.0, cz=0.0):
        TransformManager.rotate_point(
            line.start,
            angle,
            cx,
            cy,
            cz,
        )

        TransformManager.rotate_point(
            line.end,
            angle,
            cx,
            cy,
            cz,
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
    def rotate_polyline(polyline, angle, cx=0.0, cy=0.0, cz=0.0):
        for point in polyline.points:
            TransformManager.rotate_point(
                point,
                angle,
                cx,
                cy,
                cz,
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
    def rotate_circle(circle, angle, cx=0.0, cy=0.0, cz=0.0):
        TransformManager.rotate_point(
            circle.center,
            angle,
            cx,
            cy,
            cz,
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

    @staticmethod
    def rotate_element(element, angle, cx=0.0, cy=0.0, cz=0.0):
        geometry = getattr(
            element,
            "geometry",
            None
        )

        if (
            geometry is not None
            and geometry.__class__.__name__ == "Line"
        ):
            TransformManager.rotate_line(
                geometry,
                angle,
                cx,
                cy,
                cz,
            )
            return True

        element_type = element.__class__.__name__

        if element_type == "CadPolyline":
            TransformManager.rotate_polyline(
                element,
                angle,
                cx,
                cy,
                cz,
            )
            return True

        if element_type == "CadRectangle":
            TransformManager.rotate_polyline(
                element.polyline,
                angle,
                cx,
                cy,
                cz,
            )
            return True

        if element_type == "CadCircle":
            TransformManager.rotate_circle(
                element,
                angle,
                cx,
                cy,
                cz,
            )
            return True

        return False