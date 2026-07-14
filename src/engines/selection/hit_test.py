"""
AI Architecture Studio
Hit Test

Foundation 3.4
"""

import math

from engines.geometry.line import Line


class HitTest:

    @staticmethod
    def distance_point_to_line(point, line):
        x0, y0 = point.x, point.y
        x1, y1 = line.start.x, line.start.y
        x2, y2 = line.end.x, line.end.y

        dx = x2 - x1
        dy = y2 - y1

        if dx == 0 and dy == 0:
            return point.distance_to(line.start)

        t = (
            ((x0 - x1) * dx + (y0 - y1) * dy)
            / (dx * dx + dy * dy)
        )
        t = max(0.0, min(1.0, t))

        closest_x = x1 + t * dx
        closest_y = y1 + t * dy

        return math.sqrt(
            (x0 - closest_x) ** 2
            + (y0 - closest_y) ** 2
        )

    @staticmethod
    def distance_point_to_circle(point, circle):
        distance_to_center = point.distance_to(circle.center)

        return abs(
            distance_to_center - circle.radius
        )

    @staticmethod
    def distance_point_to_polyline(point, polyline):
        points = polyline.points

        if len(points) < 2:
            return None

        nearest_distance = None

        for index in range(len(points) - 1):
            segment = Line(
                points[index],
                points[index + 1]
            )

            distance = HitTest.distance_point_to_line(
                point,
                segment
            )

            if (
                nearest_distance is None
                or distance < nearest_distance
            ):
                nearest_distance = distance

        if polyline.closed and len(points) > 2:
            closing_segment = Line(
                points[-1],
                points[0]
            )

            distance = HitTest.distance_point_to_line(
                point,
                closing_segment
            )

            if (
                nearest_distance is None
                or distance < nearest_distance
            ):
                nearest_distance = distance

        return nearest_distance

    @staticmethod
    def element_distance(point, element):
        geometry = getattr(
            element,
            "geometry",
            None
        )

        if (
            geometry is not None
            and geometry.__class__.__name__ == "Line"
        ):
            return HitTest.distance_point_to_line(
                point,
                geometry
            )

        element_type = element.__class__.__name__

        if element_type == "CadPolyline":
            return HitTest.distance_point_to_polyline(
                point,
                element
            )

        if element_type == "CadRectangle":
            return HitTest.distance_point_to_polyline(
                point,
                element.polyline
            )

        if element_type == "CadCircle":
            return HitTest.distance_point_to_circle(
                point,
                element
            )

        return None

    @staticmethod
    def pick(point, scene, tolerance=0.15):
        if scene is None:
            return None

        layer_manager = None
        if scene is not None and getattr(scene, "kernel", None) is not None:
            layer_manager = scene.kernel.services.get("layer_manager")

        nearest_element = None
        nearest_distance = None

        for element in scene.get_elements():
            layer_name = getattr(element, "layer_name", "0")
            layer = None
            if layer_manager is not None:
                layer = layer_manager.get_layer(layer_name)
            if layer is not None:
                if not layer.visible or layer.locked:
                    continue

            distance = HitTest.element_distance(
                point,
                element
            )

            if distance is None:
                continue

            if distance <= tolerance:
                if (
                    nearest_distance is None
                    or distance < nearest_distance
                ):
                    nearest_element = element
                    nearest_distance = distance

        return nearest_element