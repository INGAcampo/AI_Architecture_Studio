"""
AI Architecture Studio
Transform Manager

Foundation 4.0 / MIRROR Dynamic Input 3.7
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
    def move_elements(elements, dx, dy, dz=0.0):
        """
        Mueve una colección y devuelve solamente los elementos
        que admiten transformación.
        """
        moved_elements = []

        for element in list(elements or []):
            if TransformManager.move_element(
                element,
                dx,
                dy,
                dz,
            ):
                moved_elements.append(element)

        return moved_elements

    @staticmethod
    def can_move_element(element):
        """
        Indica si el elemento es compatible con MOVE.
        """
        if element is None:
            return False

        geometry = getattr(
            element,
            "geometry",
            None,
        )

        if (
            geometry is not None
            and geometry.__class__.__name__ == "Line"
        ):
            return True

        return element.__class__.__name__ in {
            "CadPolyline",
            "CadRectangle",
            "CadCircle",
        }

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
    def rotate_elements(elements, angle, cx=0.0, cy=0.0, cz=0.0):
        rotated_elements = []

        for element in list(elements or []):
            if TransformManager.rotate_element(
                element,
                angle,
                cx,
                cy,
                cz,
            ):
                rotated_elements.append(element)

        return rotated_elements

    @staticmethod
    def can_rotate_element(element):
        return TransformManager.can_move_element(element)

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
            TransformManager.scale_polyline(
                element.polyline,
                scale,
                cx,
                cy,
                cz,
            )

            if getattr(element, "width", None) is not None:
                element.width *= abs(scale)

            if getattr(element, "height", None) is not None:
                element.height *= abs(scale)

            return True

        if element_type == "CadCircle":
            TransformManager.scale_circle(
                element,
                scale,
                cx,
                cy,
                cz,
            )
            return True

        return False

    @staticmethod
    def scale_elements(elements, scale, cx=0.0, cy=0.0, cz=0.0):
        """
        Escala una colección y devuelve únicamente
        los elementos compatibles.
        """
        scaled_elements = []

        for element in list(elements or []):
            if TransformManager.scale_element(
                element,
                scale,
                cx,
                cy,
                cz,
            ):
                scaled_elements.append(element)

        return scaled_elements

    @staticmethod
    def can_scale_element(element):
        """
        Indica si el elemento es compatible con SCALE.
        """
        return TransformManager.can_move_element(element)

    # ---------------------------------------------------------
    # MIRROR
    # ---------------------------------------------------------

    @staticmethod
    def mirror_point(point, axis_start, axis_end):
        """
        Refleja un punto respecto a una línea infinita definida
        por axis_start y axis_end.
        """
        ax = float(axis_start.x)
        ay = float(axis_start.y)
        bx = float(axis_end.x)
        by = float(axis_end.y)

        vx = bx - ax
        vy = by - ay
        length_squared = vx * vx + vy * vy

        if length_squared <= 1.0e-12:
            return False

        px = float(point.x)
        py = float(point.y)

        projection = (
            (px - ax) * vx
            + (py - ay) * vy
        ) / length_squared

        projected_x = ax + projection * vx
        projected_y = ay + projection * vy

        point.x = 2.0 * projected_x - px
        point.y = 2.0 * projected_y - py

        return True

    @staticmethod
    def mirror_line(line, axis_start, axis_end):
        start_ok = TransformManager.mirror_point(
            line.start,
            axis_start,
            axis_end,
        )
        end_ok = TransformManager.mirror_point(
            line.end,
            axis_start,
            axis_end,
        )

        return start_ok and end_ok

    @staticmethod
    def mirror_polyline(polyline, axis_start, axis_end):
        for point in polyline.points:
            if not TransformManager.mirror_point(
                point,
                axis_start,
                axis_end,
            ):
                return False

        return True

    @staticmethod
    def mirror_circle(circle, axis_start, axis_end):
        return TransformManager.mirror_point(
            circle.center,
            axis_start,
            axis_end,
        )

    @staticmethod
    def mirror_element(element, axis_start, axis_end):
        geometry = getattr(
            element,
            "geometry",
            None,
        )

        if (
            geometry is not None
            and geometry.__class__.__name__ == "Line"
        ):
            return TransformManager.mirror_line(
                geometry,
                axis_start,
                axis_end,
            )

        element_type = element.__class__.__name__

        if element_type == "CadPolyline":
            return TransformManager.mirror_polyline(
                element,
                axis_start,
                axis_end,
            )

        if element_type == "CadRectangle":
            mirrored = TransformManager.mirror_polyline(
                element.polyline,
                axis_start,
                axis_end,
            )

            if (
                mirrored
                and getattr(
                    element,
                    "angle_degrees",
                    None,
                ) is not None
            ):
                axis_angle = math.degrees(
                    math.atan2(
                        axis_end.y - axis_start.y,
                        axis_end.x - axis_start.x,
                    )
                )

                element.angle_degrees = (
                    2.0 * axis_angle
                    - element.angle_degrees
                ) % 360.0

            return mirrored

        if element_type == "CadCircle":
            return TransformManager.mirror_circle(
                element,
                axis_start,
                axis_end,
            )

        return False

    @staticmethod
    def mirror_elements(elements, axis_start, axis_end):
        """
        Refleja una colección y devuelve únicamente
        los elementos compatibles.
        """
        mirrored_elements = []

        for element in list(elements or []):
            if TransformManager.mirror_element(
                element,
                axis_start,
                axis_end,
            ):
                mirrored_elements.append(element)

        return mirrored_elements

    @staticmethod
    def can_mirror_element(element):
        """
        Indica si el elemento es compatible con MIRROR.
        """
        return TransformManager.can_move_element(element)

