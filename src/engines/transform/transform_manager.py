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

    @staticmethod
    def scale_point(point, scale, cx=0.0, cy=0.0, cz=0.0):
        dx = point.x - cx
        dy = point.y - cy
        dz = point.z - cz

        point.x = cx + dx * scale
        point.y = cy + dy * scale
        point.z = cz + dz * scale

    @staticmethod
    def scale_line(line, scale, cx=0.0, cy=0.0, cz=0.0):
        TransformManager.scale_point(line.start, scale, cx, cy, cz)
        TransformManager.scale_point(line.end, scale, cx, cy, cz)

    @staticmethod
    def scale_polyline(polyline, scale, cx=0.0, cy=0.0, cz=0.0):
        for point in polyline.points:
            TransformManager.scale_point(point, scale, cx, cy, cz)

    @staticmethod
    def scale_circle(circle, scale, cx=0.0, cy=0.0, cz=0.0):
        TransformManager.scale_point(circle.center, scale, cx, cy, cz)
        circle.radius *= scale

    @staticmethod
    def scale_element(element, scale, cx=0.0, cy=0.0, cz=0.0):
        geometry = getattr(element, "geometry", None)

        if geometry is not None and geometry.__class__.__name__ == "Line":
            TransformManager.scale_line(geometry, scale, cx, cy, cz)
            return True

        element_type = element.__class__.__name__

        if element_type == "CadPolyline":
            TransformManager.scale_polyline(element, scale, cx, cy, cz)
            return True

        if element_type == "CadRectangle":
            TransformManager.scale_polyline(element.polyline, scale, cx, cy, cz)
            return True

        if element_type == "CadCircle":
            TransformManager.scale_circle(element, scale, cx, cy, cz)
            return True

        return False