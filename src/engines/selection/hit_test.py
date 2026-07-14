"""
AI Architecture Studio
Hit Test

Professional Selection v1
"""

import math

from engines.geometry.line import Line


class HitTest:

    @staticmethod
    def _get_layer_manager(scene):
        if scene is None:
            return None

        kernel = getattr(scene, "kernel", None)

        if kernel is None:
            return None

        return kernel.services.get("layer_manager")

    @staticmethod
    def _element_is_selectable(element, scene):
        layer_manager = HitTest._get_layer_manager(scene)

        if layer_manager is None:
            return True

        layer_name = getattr(element, "layer_name", "0")
        layer = layer_manager.get_layer(layer_name)

        if layer is None:
            return True

        return layer.visible and not layer.locked

    @staticmethod
    def distance_point_to_line(point, line):
        x0, y0 = point.x, point.y
        x1, y1 = line.start.x, line.start.y
        x2, y2 = line.end.x, line.end.y

        dx = x2 - x1
        dy = y2 - y1

        if dx == 0 and dy == 0:
            return point.distance_to(line.start)

        parameter = (
            ((x0 - x1) * dx + (y0 - y1) * dy)
            / (dx * dx + dy * dy)
        )

        parameter = max(0.0, min(1.0, parameter))

        closest_x = x1 + parameter * dx
        closest_y = y1 + parameter * dy

        return math.hypot(
            x0 - closest_x,
            y0 - closest_y,
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
                points[index + 1],
            )

            distance = HitTest.distance_point_to_line(
                point,
                segment,
            )

            if (
                nearest_distance is None
                or distance < nearest_distance
            ):
                nearest_distance = distance

        if polyline.closed and len(points) > 2:
            closing_segment = Line(
                points[-1],
                points[0],
            )

            distance = HitTest.distance_point_to_line(
                point,
                closing_segment,
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
            None,
        )

        if (
            geometry is not None
            and geometry.__class__.__name__ == "Line"
        ):
            return HitTest.distance_point_to_line(
                point,
                geometry,
            )

        element_type = element.__class__.__name__

        if element_type == "CadPolyline":
            return HitTest.distance_point_to_polyline(
                point,
                element,
            )

        if element_type == "CadRectangle":
            return HitTest.distance_point_to_polyline(
                point,
                element.polyline,
            )

        if element_type == "CadCircle":
            return HitTest.distance_point_to_circle(
                point,
                element,
            )

        return None

    @staticmethod
    def pick(point, scene, tolerance=0.15):
        if scene is None:
            return None

        nearest_element = None
        nearest_distance = None

        for element in scene.get_elements():
            if not HitTest._element_is_selectable(
                element,
                scene,
            ):
                continue

            distance = HitTest.element_distance(
                point,
                element,
            )

            if distance is None:
                continue

            if distance > tolerance:
                continue

            if (
                nearest_distance is None
                or distance < nearest_distance
            ):
                nearest_element = element
                nearest_distance = distance

        return nearest_element

    @staticmethod
    def _element_points(element):
        geometry = getattr(
            element,
            "geometry",
            None,
        )

        if (
            geometry is not None
            and geometry.__class__.__name__ == "Line"
        ):
            return [
                geometry.start,
                geometry.end,
            ]

        element_type = element.__class__.__name__

        if element_type == "CadPolyline":
            return list(element.points)

        if element_type == "CadRectangle":
            return list(
                element.polyline.points
            )

        return []

    @staticmethod
    def element_bounds(element):
        element_type = element.__class__.__name__

        if element_type == "CadCircle":
            return (
                element.center.x - element.radius,
                element.center.y - element.radius,
                element.center.x + element.radius,
                element.center.y + element.radius,
            )

        points = HitTest._element_points(element)

        if not points:
            return None

        x_values = [point.x for point in points]
        y_values = [point.y for point in points]

        return (
            min(x_values),
            min(y_values),
            max(x_values),
            max(y_values),
        )

    @staticmethod
    def normalize_rectangle(first_point, second_point):
        return (
            min(first_point.x, second_point.x),
            min(first_point.y, second_point.y),
            max(first_point.x, second_point.x),
            max(first_point.y, second_point.y),
        )

    @staticmethod
    def _bounds_inside_rectangle(bounds, rectangle):
        (
            element_min_x,
            element_min_y,
            element_max_x,
            element_max_y,
        ) = bounds

        (
            rectangle_min_x,
            rectangle_min_y,
            rectangle_max_x,
            rectangle_max_y,
        ) = rectangle

        return (
            element_min_x >= rectangle_min_x
            and element_max_x <= rectangle_max_x
            and element_min_y >= rectangle_min_y
            and element_max_y <= rectangle_max_y
        )

    @staticmethod
    def _bounds_intersect_rectangle(bounds, rectangle):
        (
            element_min_x,
            element_min_y,
            element_max_x,
            element_max_y,
        ) = bounds

        (
            rectangle_min_x,
            rectangle_min_y,
            rectangle_max_x,
            rectangle_max_y,
        ) = rectangle

        return not (
            element_max_x < rectangle_min_x
            or element_min_x > rectangle_max_x
            or element_max_y < rectangle_min_y
            or element_min_y > rectangle_max_y
        )

    @staticmethod
    def select_window(
        first_point,
        second_point,
        scene,
        crossing=False,
    ):
        if scene is None:
            return []

        rectangle = HitTest.normalize_rectangle(
            first_point,
            second_point,
        )

        selected = []

        for element in scene.get_elements():
            if not HitTest._element_is_selectable(
                element,
                scene,
            ):
                continue

            bounds = HitTest.element_bounds(
                element
            )

            if bounds is None:
                continue

            if crossing:
                matches = (
                    HitTest._bounds_intersect_rectangle(
                        bounds,
                        rectangle,
                    )
                )
            else:
                matches = (
                    HitTest._bounds_inside_rectangle(
                        bounds,
                        rectangle,
                    )
                )

            if matches:
                selected.append(element)

        return selected