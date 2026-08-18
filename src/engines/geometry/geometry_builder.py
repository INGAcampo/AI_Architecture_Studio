"""
AI Architecture Studio
Geometry Builder

Foundation 2.8 / TRIM 3.9.1 / EXTEND Professional 4.0
"""

import math

from engines.geometry.point import Point
from engines.geometry.line import Line

from models.cad_circle import CadCircle
from models.cad_line import CadLine
from models.cad_polyline import CadPolyline
from models.cad_rectangle import CadRectangle


class GeometryBuilder:

    @staticmethod
    def create_line(start_point, end_point):
        """
        Construye una línea geométrica.
        """
        return Line(start_point, end_point)

    @staticmethod
    def create_polyline(points, closed=False):
        """
        Construye una polilínea CAD.
        """
        poly = CadPolyline()

        for point in points:
            poly.add_point(point)

        if closed:
            poly.close()

        return poly

    @staticmethod
    def create_rectangle(first_corner, second_corner):
        """
        Construye un rectángulo ortogonal mediante dos esquinas.
        """
        width = second_corner.x - first_corner.x
        height = second_corner.y - first_corner.y

        return GeometryBuilder.create_oriented_rectangle(
            first_corner,
            width,
            height,
            0.0,
        )

    @staticmethod
    def create_oriented_rectangle(
        origin,
        width,
        height,
        angle_degrees=0.0,
    ):
        """
        Construye un rectángulo a partir de origen, ancho,
        alto y ángulo de orientación.
        """
        radians = math.radians(angle_degrees)

        ux = math.cos(radians)
        uy = math.sin(radians)

        vx = -uy
        vy = ux

        p1 = Point(
            origin.x,
            origin.y,
            origin.z,
        )

        p2 = Point(
            origin.x + width * ux,
            origin.y + width * uy,
            origin.z,
        )

        p3 = Point(
            p2.x + height * vx,
            p2.y + height * vy,
            origin.z,
        )

        p4 = Point(
            origin.x + height * vx,
            origin.y + height * vy,
            origin.z,
        )

        poly = CadPolyline()

        for point in (p1, p2, p3, p4):
            poly.add_point(point)

        poly.close()

        return CadRectangle(
            poly,
            width=abs(width),
            height=abs(height),
            angle_degrees=angle_degrees % 360.0,
        )

    # ---------------------------------------------------------
    # OFFSET
    # ---------------------------------------------------------

    @staticmethod
    def _distance_2d(first, second):
        return math.hypot(
            second.x - first.x,
            second.y - first.y,
        )

    @staticmethod
    def _copy_point(point):
        return Point(
            point.x,
            point.y,
            point.z,
        )

    @staticmethod
    def _signed_side(first, second, point):
        """
        Devuelve un valor positivo cuando point está a la
        izquierda del segmento first -> second.
        """
        return (
            (second.x - first.x)
            * (point.y - first.y)
            - (second.y - first.y)
            * (point.x - first.x)
        )

    @staticmethod
    def _offset_segment(first, second, signed_distance):
        dx = second.x - first.x
        dy = second.y - first.y
        length = math.hypot(dx, dy)

        if length <= 1.0e-12:
            return None

        nx = -dy / length
        ny = dx / length

        start = Point(
            first.x + nx * signed_distance,
            first.y + ny * signed_distance,
            first.z,
        )

        end = Point(
            second.x + nx * signed_distance,
            second.y + ny * signed_distance,
            second.z,
        )

        return start, end

    @staticmethod
    def _line_intersection(first_a, first_b, second_a, second_b):
        x1, y1 = first_a.x, first_a.y
        x2, y2 = first_b.x, first_b.y
        x3, y3 = second_a.x, second_a.y
        x4, y4 = second_b.x, second_b.y

        denominator = (
            (x1 - x2) * (y3 - y4)
            - (y1 - y2) * (x3 - x4)
        )

        if abs(denominator) <= 1.0e-12:
            return None

        determinant_first = x1 * y2 - y1 * x2
        determinant_second = x3 * y4 - y3 * x4

        x = (
            determinant_first * (x3 - x4)
            - (x1 - x2) * determinant_second
        ) / denominator

        y = (
            determinant_first * (y3 - y4)
            - (y1 - y2) * determinant_second
        ) / denominator

        return Point(
            x,
            y,
            first_a.z,
        )

    @staticmethod
    def _nearest_segment_index(points, side_point, closed=False):
        segment_count = len(points) if closed else len(points) - 1

        if segment_count <= 0:
            return None

        best_index = None
        best_distance_squared = None

        for index in range(segment_count):
            first = points[index]
            second = points[(index + 1) % len(points)]

            dx = second.x - first.x
            dy = second.y - first.y
            length_squared = dx * dx + dy * dy

            if length_squared <= 1.0e-12:
                continue

            projection = (
                (side_point.x - first.x) * dx
                + (side_point.y - first.y) * dy
            ) / length_squared

            projection = max(0.0, min(1.0, projection))

            nearest_x = first.x + projection * dx
            nearest_y = first.y + projection * dy

            distance_squared = (
                (side_point.x - nearest_x) ** 2
                + (side_point.y - nearest_y) ** 2
            )

            if (
                best_distance_squared is None
                or distance_squared < best_distance_squared
            ):
                best_distance_squared = distance_squared
                best_index = index

        return best_index

    @staticmethod
    def create_offset_line(cad_line, distance, side_point):
        geometry = cad_line.geometry

        side = GeometryBuilder._signed_side(
            geometry.start,
            geometry.end,
            side_point,
        )

        signed_distance = (
            abs(distance)
            if side >= 0.0
            else -abs(distance)
        )

        segment = GeometryBuilder._offset_segment(
            geometry.start,
            geometry.end,
            signed_distance,
        )

        if segment is None:
            return None

        return CadLine(
            Line(segment[0], segment[1])
        )

    @staticmethod
    def create_offset_circle(circle, distance, side_point):
        cursor_radius = GeometryBuilder._distance_2d(
            circle.center,
            side_point,
        )

        if cursor_radius >= circle.radius:
            new_radius = circle.radius + abs(distance)
        else:
            new_radius = circle.radius - abs(distance)

        if new_radius <= 1.0e-9:
            return None

        return CadCircle(
            center=GeometryBuilder._copy_point(
                circle.center
            ),
            radius=new_radius,
        )

    @staticmethod
    def create_offset_polyline(polyline, distance, side_point):
        points = list(polyline.points)

        if len(points) < 2:
            return None

        closed = bool(polyline.closed)

        nearest_index = GeometryBuilder._nearest_segment_index(
            points,
            side_point,
            closed=closed,
        )

        if nearest_index is None:
            return None

        first = points[nearest_index]
        second = points[
            (nearest_index + 1) % len(points)
        ]

        side = GeometryBuilder._signed_side(
            first,
            second,
            side_point,
        )

        signed_distance = (
            abs(distance)
            if side >= 0.0
            else -abs(distance)
        )

        segment_count = len(points) if closed else len(points) - 1
        offset_segments = []

        for index in range(segment_count):
            segment = GeometryBuilder._offset_segment(
                points[index],
                points[(index + 1) % len(points)],
                signed_distance,
            )

            if segment is None:
                return None

            offset_segments.append(segment)

        result_points = []

        if closed:
            for index in range(segment_count):
                previous_segment = offset_segments[
                    (index - 1) % segment_count
                ]
                current_segment = offset_segments[index]

                intersection = GeometryBuilder._line_intersection(
                    previous_segment[0],
                    previous_segment[1],
                    current_segment[0],
                    current_segment[1],
                )

                if intersection is None:
                    intersection = GeometryBuilder._copy_point(
                        current_segment[0]
                    )

                result_points.append(intersection)

        else:
            result_points.append(
                GeometryBuilder._copy_point(
                    offset_segments[0][0]
                )
            )

            for index in range(1, segment_count):
                previous_segment = offset_segments[index - 1]
                current_segment = offset_segments[index]

                intersection = GeometryBuilder._line_intersection(
                    previous_segment[0],
                    previous_segment[1],
                    current_segment[0],
                    current_segment[1],
                )

                if intersection is None:
                    intersection = GeometryBuilder._copy_point(
                        current_segment[0]
                    )

                result_points.append(intersection)

            result_points.append(
                GeometryBuilder._copy_point(
                    offset_segments[-1][1]
                )
            )

        result = CadPolyline()

        for point in result_points:
            result.add_point(point)

        if closed:
            result.close()

        return result

    @staticmethod
    def create_offset_rectangle(rectangle, distance, side_point):
        polyline = GeometryBuilder.create_offset_polyline(
            rectangle.polyline,
            distance,
            side_point,
        )

        if (
            polyline is None
            or len(polyline.points) < 4
        ):
            return None

        p1 = polyline.points[0]
        p2 = polyline.points[1]
        p3 = polyline.points[2]

        width = GeometryBuilder._distance_2d(
            p1,
            p2,
        )
        height = GeometryBuilder._distance_2d(
            p2,
            p3,
        )
        angle_degrees = math.degrees(
            math.atan2(
                p2.y - p1.y,
                p2.x - p1.x,
            )
        ) % 360.0

        return CadRectangle(
            polyline,
            width=width,
            height=height,
            angle_degrees=angle_degrees,
        )

    @staticmethod
    def create_offset_element(element, distance, side_point):
        """
        Crea un nuevo objeto desplazado, conservando el original.
        """
        if element is None or distance <= 0.0:
            return None

        geometry = getattr(
            element,
            "geometry",
            None,
        )

        if (
            geometry is not None
            and geometry.__class__.__name__ == "Line"
        ):
            return GeometryBuilder.create_offset_line(
                element,
                distance,
                side_point,
            )

        element_type = element.__class__.__name__

        if element_type == "CadPolyline":
            return GeometryBuilder.create_offset_polyline(
                element,
                distance,
                side_point,
            )

        if element_type == "CadRectangle":
            return GeometryBuilder.create_offset_rectangle(
                element,
                distance,
                side_point,
            )

        if element_type == "CadCircle":
            return GeometryBuilder.create_offset_circle(
                element,
                distance,
                side_point,
            )

        return None

    @staticmethod
    def can_offset_element(element):
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

    # ---------------------------------------------------------
    # TRIM
    # ---------------------------------------------------------

    @staticmethod
    def _clamp(value, minimum=0.0, maximum=1.0):
        return max(minimum, min(maximum, value))

    @staticmethod
    def _point_on_segment(first, second, parameter):
        return Point(
            first.x + (second.x - first.x) * parameter,
            first.y + (second.y - first.y) * parameter,
            first.z + (second.z - first.z) * parameter,
        )

    @staticmethod
    def _segment_parameter(first, second, point):
        dx = second.x - first.x
        dy = second.y - first.y
        length_squared = dx * dx + dy * dy

        if length_squared <= 1.0e-12:
            return 0.0

        return (
            (point.x - first.x) * dx
            + (point.y - first.y) * dy
        ) / length_squared

    @staticmethod
    def _distance_point_to_segment(point, first, second):
        parameter = GeometryBuilder._clamp(
            GeometryBuilder._segment_parameter(
                first,
                second,
                point,
            )
        )

        nearest = GeometryBuilder._point_on_segment(
            first,
            second,
            parameter,
        )

        return math.hypot(
            point.x - nearest.x,
            point.y - nearest.y,
        )

    @staticmethod
    def element_segments(element):
        """
        Convierte LINE, PLINE y RECTANGLE en segmentos geométricos.
        """
        if element is None:
            return []

        geometry = getattr(element, "geometry", None)

        if (
            geometry is not None
            and geometry.__class__.__name__ == "Line"
        ):
            return [
                (
                    geometry.start,
                    geometry.end,
                )
            ]

        element_type = element.__class__.__name__

        if element_type == "CadRectangle":
            polyline = element.polyline
        elif element_type == "CadPolyline":
            polyline = element
        else:
            return []

        points = list(polyline.points)

        if len(points) < 2:
            return []

        segments = [
            (points[index], points[index + 1])
            for index in range(len(points) - 1)
        ]

        if polyline.closed:
            segments.append(
                (points[-1], points[0])
            )

        return segments

    @staticmethod
    def distance_to_element(element, point):
        """
        Distancia 2D usada por TRIM para escoger el objeto
        señalado por el cursor.
        """
        segments = GeometryBuilder.element_segments(element)

        if segments:
            return min(
                GeometryBuilder._distance_point_to_segment(
                    point,
                    first,
                    second,
                )
                for first, second in segments
            )

        if element.__class__.__name__ == "CadCircle":
            center_distance = math.hypot(
                point.x - element.center.x,
                point.y - element.center.y,
            )
            return abs(
                center_distance - element.radius
            )

        return float("inf")

    @staticmethod
    def _segment_segment_intersection_parameter(
        target_start,
        target_end,
        cutter_start,
        cutter_end,
    ):
        """
        Devuelve el parámetro t sobre el segmento objetivo.
        Solo considera intersecciones dentro de ambos segmentos.
        """
        rx = target_end.x - target_start.x
        ry = target_end.y - target_start.y
        sx = cutter_end.x - cutter_start.x
        sy = cutter_end.y - cutter_start.y

        denominator = rx * sy - ry * sx

        if abs(denominator) <= 1.0e-12:
            return None

        qpx = cutter_start.x - target_start.x
        qpy = cutter_start.y - target_start.y

        t = (qpx * sy - qpy * sx) / denominator
        u = (qpx * ry - qpy * rx) / denominator

        tolerance = 1.0e-9

        if (
            -tolerance <= t <= 1.0 + tolerance
            and -tolerance <= u <= 1.0 + tolerance
        ):
            return GeometryBuilder._clamp(t)

        return None

    @staticmethod
    def _segment_circle_intersection_parameters(
        start,
        end,
        circle,
    ):
        dx = end.x - start.x
        dy = end.y - start.y

        fx = start.x - circle.center.x
        fy = start.y - circle.center.y

        a = dx * dx + dy * dy

        if a <= 1.0e-12:
            return []

        b = 2.0 * (fx * dx + fy * dy)
        c = (
            fx * fx
            + fy * fy
            - circle.radius * circle.radius
        )

        discriminant = b * b - 4.0 * a * c

        if discriminant < -1.0e-12:
            return []

        if abs(discriminant) <= 1.0e-12:
            roots = [
                -b / (2.0 * a)
            ]
        else:
            square_root = math.sqrt(
                max(0.0, discriminant)
            )
            roots = [
                (-b - square_root) / (2.0 * a),
                (-b + square_root) / (2.0 * a),
            ]

        parameters = []

        for value in roots:
            if -1.0e-9 <= value <= 1.0 + 1.0e-9:
                parameters.append(
                    GeometryBuilder._clamp(value)
                )

        return parameters

    @staticmethod
    def _unique_parameters(parameters):
        values = []

        for parameter in sorted(parameters):
            if (
                not values
                or abs(parameter - values[-1]) > 1.0e-8
            ):
                values.append(parameter)

        return values

    @staticmethod
    def trim_line_segment(
        start,
        end,
        cutting_elements,
        pick_point,
    ):
        """
        Recorta el intervalo del segmento señalado por pick_point.
        Devuelve cero, una o dos CadLine.
        """
        intersections = []

        for cutter in cutting_elements:
            cutter_type = cutter.__class__.__name__

            if cutter_type == "CadCircle":
                intersections.extend(
                    GeometryBuilder
                    ._segment_circle_intersection_parameters(
                        start,
                        end,
                        cutter,
                    )
                )
                continue

            for cutter_start, cutter_end in (
                GeometryBuilder.element_segments(cutter)
            ):
                parameter = (
                    GeometryBuilder
                    ._segment_segment_intersection_parameter(
                        start,
                        end,
                        cutter_start,
                        cutter_end,
                    )
                )

                if parameter is not None:
                    intersections.append(parameter)

        intersections = GeometryBuilder._unique_parameters(
            parameter
            for parameter in intersections
            if 1.0e-8 < parameter < 1.0 - 1.0e-8
        )

        if not intersections:
            return None

        boundaries = [0.0] + intersections + [1.0]
        pick_parameter = GeometryBuilder._clamp(
            GeometryBuilder._segment_parameter(
                start,
                end,
                pick_point,
            )
        )

        remove_index = None

        for index in range(len(boundaries) - 1):
            lower = boundaries[index]
            upper = boundaries[index + 1]

            if (
                lower - 1.0e-9
                <= pick_parameter
                <= upper + 1.0e-9
            ):
                remove_index = index
                break

        if remove_index is None:
            return None

        result = []

        for index in range(len(boundaries) - 1):
            if index == remove_index:
                continue

            lower = boundaries[index]
            upper = boundaries[index + 1]

            if upper - lower <= 1.0e-9:
                continue

            first = GeometryBuilder._point_on_segment(
                start,
                end,
                lower,
            )
            second = GeometryBuilder._point_on_segment(
                start,
                end,
                upper,
            )

            result.append(
                CadLine(
                    Line(first, second)
                )
            )

        return result

    @staticmethod
    def trim_element(
        element,
        cutting_elements,
        pick_point,
    ):
        """
        Recorta LINE directamente.

        PLINE y RECTANGLE se convierten en segmentos CadLine:
        el segmento señalado se recorta y el resto se conserva.
        Esto evita geometrías inválidas y mantiene Undo/Redo seguro.
        """
        if element is None:
            return None

        if element.__class__.__name__ == "CadCircle":
            # El modelo actual no dispone todavía de CadArc.
            return None

        segments = GeometryBuilder.element_segments(element)

        if not segments:
            return None

        nearest_index = min(
            range(len(segments)),
            key=lambda index: (
                GeometryBuilder._distance_point_to_segment(
                    pick_point,
                    segments[index][0],
                    segments[index][1],
                )
            ),
        )

        target_start, target_end = segments[nearest_index]

        trimmed_segment = GeometryBuilder.trim_line_segment(
            target_start,
            target_end,
            cutting_elements,
            pick_point,
        )

        if trimmed_segment is None:
            return None

        geometry = getattr(element, "geometry", None)

        if (
            geometry is not None
            and geometry.__class__.__name__ == "Line"
        ):
            return trimmed_segment

        result = []

        for index, (first, second) in enumerate(segments):
            if index == nearest_index:
                result.extend(trimmed_segment)
            else:
                result.append(
                    CadLine(
                        Line(
                            GeometryBuilder._copy_point(first),
                            GeometryBuilder._copy_point(second),
                        )
                    )
                )

        return result

    @staticmethod
    def can_trim_element(element):
        if element is None:
            return False

        geometry = getattr(element, "geometry", None)

        if (
            geometry is not None
            and geometry.__class__.__name__ == "Line"
        ):
            return True

        return element.__class__.__name__ in {
            "CadPolyline",
            "CadRectangle",
        }

    @staticmethod
    def can_be_cutting_edge(element):
        if GeometryBuilder.can_trim_element(element):
            return True

        return (
            element is not None
            and element.__class__.__name__ == "CadCircle"
        )

    # ---------------------------------------------------------
    # EXTEND PROFESSIONAL 4.0
    # ---------------------------------------------------------

    @staticmethod
    def _ray_segment_intersection_parameter(
        ray_start,
        ray_dx,
        ray_dy,
        segment_start,
        segment_end,
    ):
        """
        Devuelve la distancia paramétrica t sobre un rayo:

            P(t) = ray_start + t * ray_direction

        Solo acepta t > 0 y una intersección situada dentro del
        segmento límite.
        """
        sx = segment_end.x - segment_start.x
        sy = segment_end.y - segment_start.y

        denominator = ray_dx * sy - ray_dy * sx

        if abs(denominator) <= 1.0e-12:
            return None

        qpx = segment_start.x - ray_start.x
        qpy = segment_start.y - ray_start.y

        t = (qpx * sy - qpy * sx) / denominator
        u = (qpx * ray_dy - qpy * ray_dx) / denominator

        tolerance = 1.0e-9

        if (
            t > tolerance
            and -tolerance <= u <= 1.0 + tolerance
        ):
            return t

        return None

    @staticmethod
    def _ray_circle_intersection_parameters(
        ray_start,
        ray_dx,
        ray_dy,
        circle,
    ):
        """
        Intersecciones positivas entre un rayo y un círculo.
        """
        fx = ray_start.x - circle.center.x
        fy = ray_start.y - circle.center.y

        a = ray_dx * ray_dx + ray_dy * ray_dy

        if a <= 1.0e-12:
            return []

        b = 2.0 * (fx * ray_dx + fy * ray_dy)
        c = (
            fx * fx
            + fy * fy
            - circle.radius * circle.radius
        )

        discriminant = b * b - 4.0 * a * c

        if discriminant < -1.0e-12:
            return []

        if abs(discriminant) <= 1.0e-12:
            roots = [-b / (2.0 * a)]
        else:
            root = math.sqrt(max(0.0, discriminant))
            roots = [
                (-b - root) / (2.0 * a),
                (-b + root) / (2.0 * a),
            ]

        return [
            value
            for value in roots
            if value > 1.0e-9
        ]

    @staticmethod
    def extend_line(
        element,
        boundary_elements,
        pick_point,
    ):
        """
        Extiende el extremo de una CadLine señalado por el cursor
        hasta el límite válido más cercano.

        Los límites pueden ser:
        LINE, PLINE, RECTANGLE o CIRCLE.
        """
        if element is None:
            return None

        geometry = getattr(element, "geometry", None)

        if (
            geometry is None
            or geometry.__class__.__name__ != "Line"
        ):
            return None

        start = geometry.start
        end = geometry.end

        distance_to_start = GeometryBuilder._distance_2d(
            pick_point,
            start,
        )
        distance_to_end = GeometryBuilder._distance_2d(
            pick_point,
            end,
        )

        if distance_to_start <= distance_to_end:
            fixed_point = end
            moving_point = start
        else:
            fixed_point = start
            moving_point = end

        ray_dx = moving_point.x - fixed_point.x
        ray_dy = moving_point.y - fixed_point.y
        ray_length = math.hypot(ray_dx, ray_dy)

        if ray_length <= 1.0e-12:
            return None

        ray_dx /= ray_length
        ray_dy /= ray_length

        candidates = []

        for boundary in boundary_elements:
            if boundary is element:
                continue

            if boundary.__class__.__name__ == "CadCircle":
                for parameter in (
                    GeometryBuilder
                    ._ray_circle_intersection_parameters(
                        moving_point,
                        ray_dx,
                        ray_dy,
                        boundary,
                    )
                ):
                    candidates.append(parameter)

                continue

            for first, second in (
                GeometryBuilder.element_segments(boundary)
            ):
                parameter = (
                    GeometryBuilder
                    ._ray_segment_intersection_parameter(
                        moving_point,
                        ray_dx,
                        ray_dy,
                        first,
                        second,
                    )
                )

                if parameter is not None:
                    candidates.append(parameter)

        if not candidates:
            return None

        nearest = min(candidates)

        extended_point = Point(
            moving_point.x + ray_dx * nearest,
            moving_point.y + ray_dy * nearest,
            moving_point.z,
        )

        if distance_to_start <= distance_to_end:
            new_start = extended_point
            new_end = GeometryBuilder._copy_point(end)
        else:
            new_start = GeometryBuilder._copy_point(start)
            new_end = extended_point

        return CadLine(
            Line(new_start, new_end)
        )

    @staticmethod
    def extend_element(
        element,
        boundary_elements,
        pick_point,
    ):
        """
        Punto de entrada universal para EXTEND 4.0.
        La primera versión profesional extiende CadLine.
        """
        if not GeometryBuilder.can_extend_element(element):
            return None

        return GeometryBuilder.extend_line(
            element,
            boundary_elements,
            pick_point,
        )

    @staticmethod
    def can_extend_element(element):
        if element is None:
            return False

        geometry = getattr(element, "geometry", None)

        return (
            geometry is not None
            and geometry.__class__.__name__ == "Line"
        )

    @staticmethod
    def can_be_extension_boundary(element):
        """
        LINE, PLINE, RECTANGLE y CIRCLE pueden actuar como
        límites de extensión.
        """
        return GeometryBuilder.can_be_cutting_edge(element)

    # ---------------------------------------------------------
    # FILLET PROFESSIONAL 4.1
    # ---------------------------------------------------------

    @staticmethod
    def _cross_2d(ax, ay, bx, by):
        return ax * by - ay * bx

    @staticmethod
    def _dot_2d(ax, ay, bx, by):
        return ax * bx + ay * by

    @staticmethod
    def _normalize_2d(x, y):
        length = math.hypot(x, y)

        if length <= 1.0e-12:
            return None

        return x / length, y / length

    @staticmethod
    def _infinite_line_intersection(
        first_start,
        first_end,
        second_start,
        second_end,
    ):
        rx = first_end.x - first_start.x
        ry = first_end.y - first_start.y
        sx = second_end.x - second_start.x
        sy = second_end.y - second_start.y

        denominator = GeometryBuilder._cross_2d(
            rx,
            ry,
            sx,
            sy,
        )

        if abs(denominator) <= 1.0e-12:
            return None

        qpx = second_start.x - first_start.x
        qpy = second_start.y - first_start.y

        parameter = GeometryBuilder._cross_2d(
            qpx,
            qpy,
            sx,
            sy,
        ) / denominator

        return Point(
            first_start.x + parameter * rx,
            first_start.y + parameter * ry,
            first_start.z,
        )

    @staticmethod
    def _ray_direction_from_pick(
        intersection,
        line,
        pick_point,
    ):
        dx = line.end.x - line.start.x
        dy = line.end.y - line.start.y

        normalized = GeometryBuilder._normalize_2d(dx, dy)

        if normalized is None:
            return None

        ux, uy = normalized

        pick_dx = pick_point.x - intersection.x
        pick_dy = pick_point.y - intersection.y

        if GeometryBuilder._dot_2d(
            pick_dx,
            pick_dy,
            ux,
            uy,
        ) < 0.0:
            ux = -ux
            uy = -uy

        return ux, uy

    @staticmethod
    def _replace_line_corner(
        cad_line,
        intersection,
        tangent_point,
        ray_direction,
    ):
        """
        Conserva el extremo situado en la rama seleccionada y
        reemplaza el extremo próximo a la esquina por la tangencia.
        """
        line = cad_line.geometry
        ux, uy = ray_direction

        start_projection = GeometryBuilder._dot_2d(
            line.start.x - intersection.x,
            line.start.y - intersection.y,
            ux,
            uy,
        )
        end_projection = GeometryBuilder._dot_2d(
            line.end.x - intersection.x,
            line.end.y - intersection.y,
            ux,
            uy,
        )

        if start_projection >= end_projection:
            outer = GeometryBuilder._copy_point(line.start)

            return CadLine(
                Line(
                    outer,
                    GeometryBuilder._copy_point(
                        tangent_point
                    ),
                )
            )

        outer = GeometryBuilder._copy_point(line.end)

        return CadLine(
            Line(
                GeometryBuilder._copy_point(
                    tangent_point
                ),
                outer,
            )
        )

    @staticmethod
    def create_fillet(
        first_element,
        second_element,
        first_pick,
        second_pick,
        radius,
    ):
        """
        Crea un empalme tangente entre dos CadLine.

        Retorna:
            (new_first, new_second, arc)

        Para radio 0 retorna:
            (new_first, new_second, None)
        """
        from models.cad_arc import CadArc

        if (
            not GeometryBuilder.can_fillet_element(first_element)
            or not GeometryBuilder.can_fillet_element(second_element)
            or first_element is second_element
        ):
            return None

        radius = float(radius)

        if radius < 0.0:
            return None

        first_line = first_element.geometry
        second_line = second_element.geometry

        intersection = (
            GeometryBuilder._infinite_line_intersection(
                first_line.start,
                first_line.end,
                second_line.start,
                second_line.end,
            )
        )

        if intersection is None:
            return None

        first_ray = GeometryBuilder._ray_direction_from_pick(
            intersection,
            first_line,
            first_pick,
        )
        second_ray = GeometryBuilder._ray_direction_from_pick(
            intersection,
            second_line,
            second_pick,
        )

        if first_ray is None or second_ray is None:
            return None

        u1x, u1y = first_ray
        u2x, u2y = second_ray

        dot = max(
            -1.0,
            min(
                1.0,
                GeometryBuilder._dot_2d(
                    u1x,
                    u1y,
                    u2x,
                    u2y,
                ),
            ),
        )

        angle = math.acos(dot)

        if (
            angle <= 1.0e-8
            or abs(math.pi - angle) <= 1.0e-8
        ):
            return None

        if radius <= 1.0e-12:
            corner = GeometryBuilder._copy_point(
                intersection
            )

            first_result = (
                GeometryBuilder._replace_line_corner(
                    first_element,
                    intersection,
                    corner,
                    first_ray,
                )
            )
            second_result = (
                GeometryBuilder._replace_line_corner(
                    second_element,
                    intersection,
                    corner,
                    second_ray,
                )
            )

            return first_result, second_result, None

        tangent_distance = (
            radius / math.tan(angle / 2.0)
        )

        tangent_1 = Point(
            intersection.x + u1x * tangent_distance,
            intersection.y + u1y * tangent_distance,
            intersection.z,
        )
        tangent_2 = Point(
            intersection.x + u2x * tangent_distance,
            intersection.y + u2y * tangent_distance,
            intersection.z,
        )

        bisector_x = u1x + u2x
        bisector_y = u1y + u2y
        bisector = GeometryBuilder._normalize_2d(
            bisector_x,
            bisector_y,
        )

        if bisector is None:
            return None

        bx, by = bisector
        center_distance = radius / math.sin(angle / 2.0)

        center = Point(
            intersection.x + bx * center_distance,
            intersection.y + by * center_distance,
            intersection.z,
        )

        start_angle = math.atan2(
            tangent_1.y - center.y,
            tangent_1.x - center.x,
        )
        end_angle = math.atan2(
            tangent_2.y - center.y,
            tangent_2.x - center.x,
        )

        radius_1_x = tangent_1.x - center.x
        radius_1_y = tangent_1.y - center.y
        radius_2_x = tangent_2.x - center.x
        radius_2_y = tangent_2.y - center.y

        clockwise = (
            GeometryBuilder._cross_2d(
                radius_1_x,
                radius_1_y,
                radius_2_x,
                radius_2_y,
            )
            < 0.0
        )

        arc = CadArc(
            center,
            radius,
            start_angle,
            end_angle,
            clockwise,
        )

        first_result = (
            GeometryBuilder._replace_line_corner(
                first_element,
                intersection,
                tangent_1,
                first_ray,
            )
        )
        second_result = (
            GeometryBuilder._replace_line_corner(
                second_element,
                intersection,
                tangent_2,
                second_ray,
            )
        )

        return first_result, second_result, arc

    @staticmethod
    def can_fillet_element(element):
        if element is None:
            return False

        geometry = getattr(element, "geometry", None)

        return (
            geometry is not None
            and geometry.__class__.__name__ == "Line"
        )

    # ---------------------------------------------------------
    # FILLET PLINE PROFESSIONAL 4.1.1
    # ---------------------------------------------------------

    @staticmethod
    def polyline_segment_records(element):
        """
        Retorna los segmentos LINE seleccionables de una PLINE:
        [(index, Line), ...]
        """
        if element is None:
            return []

        if element.__class__.__name__ != "CadPolyline":
            return []

        getter = getattr(element, "get_segments", None)
        segments = getter() if callable(getter) else []

        return [
            (index, segment)
            for index, segment in enumerate(segments)
            if segment.__class__.__name__ == "Line"
        ]

    @staticmethod
    def distance_to_line_segment(line, point):
        return GeometryBuilder._distance_point_to_segment(
            point,
            line.start,
            line.end,
        )

    @staticmethod
    def orient_line_like(reference, candidate):
        """
        Devuelve una copia de candidate con el mismo sentido del
        segmento reference.
        """
        start_same = reference.start.distance_to(
            candidate.start
        ) + reference.end.distance_to(candidate.end)

        reversed_same = reference.start.distance_to(
            candidate.end
        ) + reference.end.distance_to(candidate.start)

        if start_same <= reversed_same:
            return Line(
                GeometryBuilder._copy_point(candidate.start),
                GeometryBuilder._copy_point(candidate.end),
            )

        return Line(
            GeometryBuilder._copy_point(candidate.end),
            GeometryBuilder._copy_point(candidate.start),
        )

    @staticmethod
    def replace_polyline_segments(
        polyline,
        replacements_by_index,
        inserted_after=None,
    ):
        """
        Clona una PLINE y reemplaza segmentos concretos. inserted_after
        permite insertar CadArc después del índice indicado.
        """
        cloned = polyline.clone()
        source_segments = polyline.get_segments()
        output = []
        inserted_after = inserted_after or {}

        for index, segment in enumerate(source_segments):
            replacement = replacements_by_index.get(
                index,
                segment,
            )
            output.append(replacement)

            for extra in inserted_after.get(index, []):
                output.append(extra)

        cloned.set_segments(
            output,
            closed=polyline.closed,
        )
        return cloned

    @staticmethod
    def are_adjacent_polyline_segments(
        polyline,
        first_index,
        second_index,
    ):
        count = polyline.segment_count

        if count < 2 or first_index == second_index:
            return False

        if abs(first_index - second_index) == 1:
            return True

        return (
            polyline.closed
            and {first_index, second_index} == {0, count - 1}
        )

    @staticmethod
    def create_fillet_from_lines(
        first_line,
        second_line,
        first_pick,
        second_pick,
        radius,
    ):
        """
        Adaptador que permite usar el algoritmo FILLET 4.1 con
        segmentos internos de PLINE.
        """
        first_proxy = CadLine(first_line)
        second_proxy = CadLine(second_line)

        return GeometryBuilder.create_fillet(
            first_proxy,
            second_proxy,
            first_pick,
            second_pick,
            radius,
        )

    # ---------------------------------------------------------
    # CHAMFER PROFESSIONAL 4.2
    # ---------------------------------------------------------

    @staticmethod
    def create_chamfer(
        first_element,
        second_element,
        first_pick,
        second_pick,
        first_distance,
        second_distance,
    ):
        """
        Crea un chaflán entre dos CadLine.

        Retorna:
            (new_first, new_second, chamfer_line)

        Cuando ambas distancias son cero, chamfer_line es None y
        las dos líneas se unen en la intersección teórica.
        """
        if (
            not GeometryBuilder.can_chamfer_element(first_element)
            or not GeometryBuilder.can_chamfer_element(second_element)
            or first_element is second_element
        ):
            return None

        first_distance = float(first_distance)
        second_distance = float(second_distance)

        if first_distance < 0.0 or second_distance < 0.0:
            return None

        first_line = first_element.geometry
        second_line = second_element.geometry

        intersection = GeometryBuilder._infinite_line_intersection(
            first_line.start,
            first_line.end,
            second_line.start,
            second_line.end,
        )

        if intersection is None:
            return None

        first_ray = GeometryBuilder._ray_direction_from_pick(
            intersection,
            first_line,
            first_pick,
        )
        second_ray = GeometryBuilder._ray_direction_from_pick(
            intersection,
            second_line,
            second_pick,
        )

        if first_ray is None or second_ray is None:
            return None

        u1x, u1y = first_ray
        u2x, u2y = second_ray

        dot = max(
            -1.0,
            min(
                1.0,
                GeometryBuilder._dot_2d(
                    u1x,
                    u1y,
                    u2x,
                    u2y,
                ),
            ),
        )

        # Paralelas o colineales no forman una esquina válida.
        if abs(abs(dot) - 1.0) <= 1.0e-10:
            return None

        first_point = Point(
            intersection.x + u1x * first_distance,
            intersection.y + u1y * first_distance,
            intersection.z,
        )
        second_point = Point(
            intersection.x + u2x * second_distance,
            intersection.y + u2y * second_distance,
            intersection.z,
        )

        new_first = GeometryBuilder._replace_line_corner(
            first_element,
            intersection,
            first_point,
            first_ray,
        )
        new_second = GeometryBuilder._replace_line_corner(
            second_element,
            intersection,
            second_point,
            second_ray,
        )

        if (
            first_point.distance_to(second_point) <= 1.0e-10
        ):
            return new_first, new_second, None

        chamfer_line = CadLine(
            Line(
                GeometryBuilder._copy_point(first_point),
                GeometryBuilder._copy_point(second_point),
            )
        )

        return new_first, new_second, chamfer_line

    @staticmethod
    def create_chamfer_from_lines(
        first_line,
        second_line,
        first_pick,
        second_pick,
        first_distance,
        second_distance,
    ):
        """Adaptador para segmentos internos de CadPolyline."""
        return GeometryBuilder.create_chamfer(
            CadLine(first_line),
            CadLine(second_line),
            first_pick,
            second_pick,
            first_distance,
            second_distance,
        )

    @staticmethod
    def can_chamfer_element(element):
        if element is None:
            return False

        geometry = getattr(element, "geometry", None)

        return (
            geometry is not None
            and geometry.__class__.__name__ == "Line"
        )

    # ---------------------------------------------------------
    # JOIN PROFESSIONAL 4.3
    # ---------------------------------------------------------

    @staticmethod
    def _join_segment_start(segment):
        if segment.__class__.__name__ == "Line":
            return segment.start
        return getattr(segment, "start_point", None)

    @staticmethod
    def _join_segment_end(segment):
        if segment.__class__.__name__ == "Line":
            return segment.end
        return getattr(segment, "end_point", None)

    @staticmethod
    def _reverse_join_segment(segment):
        kind = segment.__class__.__name__

        if kind == "Line":
            return Line(
                GeometryBuilder._copy_point(segment.end),
                GeometryBuilder._copy_point(segment.start),
            )

        if kind == "CadArc":
            from models.cad_arc import CadArc

            return CadArc(
                GeometryBuilder._copy_point(segment.center),
                segment.radius,
                segment.end_angle,
                segment.start_angle,
                not segment.clockwise,
            )

        return None

    @staticmethod
    def _clone_join_segment(segment):
        kind = segment.__class__.__name__

        if kind == "Line":
            return Line(
                GeometryBuilder._copy_point(segment.start),
                GeometryBuilder._copy_point(segment.end),
            )

        if kind == "CadArc":
            return segment.clone()

        return None

    @staticmethod
    def joinable_segments(element):
        """
        Convierte LINE o PLINE en una secuencia ordenada de segmentos.
        """
        if element is None:
            return None

        geometry = getattr(element, "geometry", None)

        if (
            geometry is not None
            and geometry.__class__.__name__ == "Line"
        ):
            return [
                GeometryBuilder._clone_join_segment(geometry)
            ]

        if element.__class__.__name__ == "CadPolyline":
            segments = element.get_segments()

            if not segments:
                return None

            cloned = [
                GeometryBuilder._clone_join_segment(segment)
                for segment in segments
            ]

            if any(segment is None for segment in cloned):
                return None

            return cloned

        return None

    @staticmethod
    def can_join_element(element):
        return GeometryBuilder.joinable_segments(element) is not None

    @staticmethod
    def _reverse_join_chain(chain):
        return [
            GeometryBuilder._reverse_join_segment(segment)
            for segment in reversed(chain)
        ]

    @staticmethod
    def _join_chain_start(chain):
        if not chain:
            return None
        return GeometryBuilder._join_segment_start(chain[0])

    @staticmethod
    def _join_chain_end(chain):
        if not chain:
            return None
        return GeometryBuilder._join_segment_end(chain[-1])

    @staticmethod
    def _join_points_close(first, second, tolerance):
        if first is None or second is None:
            return False
        return first.distance_to(second) <= tolerance

    @staticmethod
    def _snap_join_connection(left, right):
        """
        Elimina microseparaciones haciendo coincidir los extremos
        conectados sin alterar la geometría general.
        """
        if not left or not right:
            return

        left_end = GeometryBuilder._join_segment_end(left[-1])
        right_start = GeometryBuilder._join_segment_start(right[0])

        if left_end is None or right_start is None:
            return

        point = Point(
            (left_end.x + right_start.x) * 0.5,
            (left_end.y + right_start.y) * 0.5,
            (left_end.z + right_start.z) * 0.5,
        )

        last = left[-1]
        first = right[0]

        if last.__class__.__name__ == "Line":
            last.end = GeometryBuilder._copy_point(point)

        if first.__class__.__name__ == "Line":
            first.start = GeometryBuilder._copy_point(point)

    @staticmethod
    def create_joined_polyline(elements, tolerance=0.01):
        """
        Une LINE/PLINE conectadas en una sola CadPolyline híbrida.
        Retorna None cuando las entidades forman más de una cadena.
        """
        if elements is None:
            return None

        unique = []
        seen = set()

        for element in elements:
            if id(element) in seen:
                continue
            seen.add(id(element))
            unique.append(element)

        if len(unique) < 2:
            return None

        chains = []

        for element in unique:
            segments = GeometryBuilder.joinable_segments(element)

            if not segments:
                return None

            chains.append(segments)

        chain = chains.pop(0)

        while chains:
            connected = False
            chain_start = GeometryBuilder._join_chain_start(chain)
            chain_end = GeometryBuilder._join_chain_end(chain)

            for index, candidate in enumerate(chains):
                candidate_start = GeometryBuilder._join_chain_start(
                    candidate
                )
                candidate_end = GeometryBuilder._join_chain_end(
                    candidate
                )

                if GeometryBuilder._join_points_close(
                    chain_end,
                    candidate_start,
                    tolerance,
                ):
                    GeometryBuilder._snap_join_connection(
                        chain,
                        candidate,
                    )
                    chain.extend(candidate)
                    chains.pop(index)
                    connected = True
                    break

                if GeometryBuilder._join_points_close(
                    chain_end,
                    candidate_end,
                    tolerance,
                ):
                    candidate = GeometryBuilder._reverse_join_chain(
                        candidate
                    )
                    GeometryBuilder._snap_join_connection(
                        chain,
                        candidate,
                    )
                    chain.extend(candidate)
                    chains.pop(index)
                    connected = True
                    break

                if GeometryBuilder._join_points_close(
                    chain_start,
                    candidate_end,
                    tolerance,
                ):
                    GeometryBuilder._snap_join_connection(
                        candidate,
                        chain,
                    )
                    chain = candidate + chain
                    chains.pop(index)
                    connected = True
                    break

                if GeometryBuilder._join_points_close(
                    chain_start,
                    candidate_start,
                    tolerance,
                ):
                    candidate = GeometryBuilder._reverse_join_chain(
                        candidate
                    )
                    GeometryBuilder._snap_join_connection(
                        candidate,
                        chain,
                    )
                    chain = candidate + chain
                    chains.pop(index)
                    connected = True
                    break

            if not connected:
                return None

        closed = GeometryBuilder._join_points_close(
            GeometryBuilder._join_chain_start(chain),
            GeometryBuilder._join_chain_end(chain),
            tolerance,
        )

        if closed and chain:
            first_point = GeometryBuilder._join_chain_start(chain)
            last_segment = chain[-1]

            if last_segment.__class__.__name__ == "Line":
                last_segment.end = GeometryBuilder._copy_point(
                    first_point
                )

        polyline = CadPolyline()
        polyline.set_segments(chain, closed=closed)
        return polyline

    # ---------------------------------------------------------
    # WALL JOIN PROFESSIONAL 5.0.4.2
    # ---------------------------------------------------------

    @staticmethod
    def _wall_offsets(thickness, justification="center"):
        t = float(thickness)
        mode = str(justification).strip().lower()
        if mode in {"left", "izquierda", "exterior"}:
            return t, 0.0
        if mode in {"right", "derecha", "interior"}:
            return 0.0, t
        return t / 2.0, t / 2.0

    @staticmethod
    def build_wall_offsets(points, thickness, justification="center", miter_limit=8.0):
        points = list(points or [])
        if len(points) < 2:
            return {"left": [], "right": [], "segments": []}

        left_d, right_d = GeometryBuilder._wall_offsets(thickness, justification)
        left_segments, right_segments, centers = [], [], []
        for i in range(len(points)-1):
            a, b = points[i], points[i+1]
            if GeometryBuilder._distance_2d(a, b) <= 1.0e-10:
                continue
            left = GeometryBuilder._offset_segment(a, b, left_d)
            right = GeometryBuilder._offset_segment(a, b, -right_d)
            if left is None or right is None:
                continue
            left_segments.append(left); right_segments.append(right); centers.append((a,b))

        if not centers:
            return {"left": [], "right": [], "segments": []}

        max_miter = max(float(thickness) * float(miter_limit), 1.0e-6)

        def join_vertex(vertex, previous, current):
            p = GeometryBuilder._line_intersection(previous[0], previous[1], current[0], current[1])
            if p is None or GeometryBuilder._distance_2d(vertex, p) > max_miter:
                return GeometryBuilder._copy_point(current[0])
            return p

        left_points=[GeometryBuilder._copy_point(left_segments[0][0])]
        right_points=[GeometryBuilder._copy_point(right_segments[0][0])]
        for i in range(1, len(centers)):
            vertex=centers[i][0]
            left_points.append(join_vertex(vertex, left_segments[i-1], left_segments[i]))
            right_points.append(join_vertex(vertex, right_segments[i-1], right_segments[i]))
        left_points.append(GeometryBuilder._copy_point(left_segments[-1][1]))
        right_points.append(GeometryBuilder._copy_point(right_segments[-1][1]))
        return {"left": left_points, "right": right_points, "segments": centers}

    @staticmethod
    def build_clean_wall_geometry(points, thickness, justification="center", miter_limit=8.0):
        data = GeometryBuilder.build_wall_offsets(points, thickness, justification, miter_limit)
        left, right = data["left"], data["right"]
        if len(left) < 2 or len(right) < 2:
            return []
        return [GeometryBuilder._copy_point(p) for p in left] + [GeometryBuilder._copy_point(p) for p in reversed(right)]

    @staticmethod
    def build_wall_segment_polygons(points, thickness, justification="center"):
        points=list(points or [])
        left_d, right_d = GeometryBuilder._wall_offsets(thickness, justification)
        result=[]
        for i in range(len(points)-1):
            a,b=points[i],points[i+1]
            left=GeometryBuilder._offset_segment(a,b,left_d)
            right=GeometryBuilder._offset_segment(a,b,-right_d)
            if left is None or right is None: continue
            result.append([
                GeometryBuilder._copy_point(left[0]), GeometryBuilder._copy_point(left[1]),
                GeometryBuilder._copy_point(right[1]), GeometryBuilder._copy_point(right[0]),
            ])
        return result

    @staticmethod
    def compute_wall_join(first_start, first_end, second_start, second_end, first_offset, second_offset):
        first=GeometryBuilder._offset_segment(first_start, first_end, first_offset)
        second=GeometryBuilder._offset_segment(second_start, second_end, second_offset)
        if first is None or second is None: return None
        return GeometryBuilder._line_intersection(first[0], first[1], second[0], second[1])

