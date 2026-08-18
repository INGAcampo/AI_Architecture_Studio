"""
AI Architecture Studio
CAD Engine - Object Snap

SNAP Professional v2.1
"""

import math

from engines.geometry.point import Point


class SnapEngine:

    MODE_ENDPOINT = "Endpoint"
    MODE_MIDPOINT = "Midpoint"
    MODE_CENTER = "Center"
    MODE_INTERSECTION = "Intersection"
    MODE_NEAREST = "Nearest"
    MODE_GRID = "Grid"

    # Un número menor significa mayor prioridad.
    SNAP_PRIORITY = {
        MODE_ENDPOINT: 1,
        MODE_INTERSECTION: 2,
        MODE_MIDPOINT: 3,
        MODE_CENTER: 4,
        MODE_NEAREST: 5,
        MODE_GRID: 6,
    }

    def __init__(self):
        self.enabled = True

        # Distancia máxima de captura en unidades del dibujo.
        self.snap_distance = 0.35

        self.grid_spacing = 0.25

        self.enabled_modes = {
            self.MODE_ENDPOINT,
            self.MODE_MIDPOINT,
            self.MODE_CENTER,
            self.MODE_INTERSECTION,
            self.MODE_NEAREST,
            self.MODE_GRID,
        }

    # ---------------------------------------------------------
    # ESTADO
    # ---------------------------------------------------------

    def toggle(self):
        self.enabled = not self.enabled

        state = (
            "ACTIVADO"
            if self.enabled
            else "DESACTIVADO"
        )

        print(f"SNAP {state}")

        return self.enabled

    def set_enabled(self, enabled):
        self.enabled = bool(enabled)

    def enable_mode(self, mode):
        self.enabled_modes.add(mode)

    def disable_mode(self, mode):
        self.enabled_modes.discard(mode)

    def mode_enabled(self, mode):
        return mode in self.enabled_modes

    # ---------------------------------------------------------
    # CAPAS
    # ---------------------------------------------------------

    def _element_is_visible(self, element, scene):
        kernel = getattr(
            scene,
            "kernel",
            None,
        )

        if kernel is None:
            return True

        layer_manager = kernel.services.get(
            "layer_manager"
        )

        if layer_manager is None:
            return True

        layer_name = getattr(
            element,
            "layer_name",
            "0",
        )

        layer = layer_manager.get_layer(
            layer_name
        )

        if layer is None:
            return True

        return layer.visible

    # ---------------------------------------------------------
    # SEGMENTOS DE ENTIDADES
    # ---------------------------------------------------------

    def _element_segments(self, element):
        segments = []

        geometry = getattr(
            element,
            "geometry",
            None,
        )

        if (
            geometry is not None
            and geometry.__class__.__name__ == "Line"
        ):
            segments.append(
                (
                    geometry.start,
                    geometry.end,
                )
            )

            return segments

        element_type = element.__class__.__name__

        if element_type == "CadPolyline":
            points = element.points
            closed = element.closed

        elif element_type == "CadRectangle":
            points = element.polyline.points
            closed = element.polyline.closed

        else:
            return segments

        for index in range(len(points) - 1):
            segments.append(
                (
                    points[index],
                    points[index + 1],
                )
            )

        if closed and len(points) > 2:
            segments.append(
                (
                    points[-1],
                    points[0],
                )
            )

        return segments

    def _all_segments(self, scene):
        segments = []

        if scene is None:
            return segments

        for element in scene.get_elements():
            if not self._element_is_visible(
                element,
                scene,
            ):
                continue

            for start, end in self._element_segments(
                element
            ):
                segments.append(
                    (
                        element,
                        start,
                        end,
                    )
                )

        return segments

    # ---------------------------------------------------------
    # GEOMETRÍA AUXILIAR
    # ---------------------------------------------------------

    @staticmethod
    def _midpoint(start, end):
        return Point(
            (start.x + end.x) / 2.0,
            (start.y + end.y) / 2.0,
            (start.z + end.z) / 2.0,
        )

    @staticmethod
    def _nearest_point_on_segment(
        point,
        start,
        end,
    ):
        dx = end.x - start.x
        dy = end.y - start.y

        length_squared = (
            dx * dx
            + dy * dy
        )

        if length_squared <= 1e-12:
            return Point(
                start.x,
                start.y,
                start.z,
            )

        parameter = (
            (
                (point.x - start.x) * dx
                + (point.y - start.y) * dy
            )
            / length_squared
        )

        parameter = max(
            0.0,
            min(1.0, parameter),
        )

        return Point(
            start.x + parameter * dx,
            start.y + parameter * dy,
            start.z
            + parameter * (end.z - start.z),
        )

    @staticmethod
    def _nearest_point_on_circle(
        point,
        center,
        radius,
    ):
        dx = point.x - center.x
        dy = point.y - center.y

        distance = math.hypot(
            dx,
            dy,
        )

        if distance <= 1e-12:
            return Point(
                center.x + radius,
                center.y,
                center.z,
            )

        factor = radius / distance

        return Point(
            center.x + dx * factor,
            center.y + dy * factor,
            center.z,
        )

    @staticmethod
    def _segment_intersection(
        start_1,
        end_1,
        start_2,
        end_2,
    ):
        x1, y1 = start_1.x, start_1.y
        x2, y2 = end_1.x, end_1.y
        x3, y3 = start_2.x, start_2.y
        x4, y4 = end_2.x, end_2.y

        denominator = (
            (x1 - x2) * (y3 - y4)
            - (y1 - y2) * (x3 - x4)
        )

        if abs(denominator) <= 1e-12:
            return None

        determinant_1 = (
            x1 * y2
            - y1 * x2
        )

        determinant_2 = (
            x3 * y4
            - y3 * x4
        )

        intersection_x = (
            determinant_1 * (x3 - x4)
            - (x1 - x2) * determinant_2
        ) / denominator

        intersection_y = (
            determinant_1 * (y3 - y4)
            - (y1 - y2) * determinant_2
        ) / denominator

        segment_1_length_squared = (
            (x2 - x1) ** 2
            + (y2 - y1) ** 2
        )

        segment_2_length_squared = (
            (x4 - x3) ** 2
            + (y4 - y3) ** 2
        )

        if (
            segment_1_length_squared <= 1e-12
            or segment_2_length_squared <= 1e-12
        ):
            return None

        parameter_1 = (
            (
                (intersection_x - x1)
                * (x2 - x1)
                + (intersection_y - y1)
                * (y2 - y1)
            )
            / segment_1_length_squared
        )

        parameter_2 = (
            (
                (intersection_x - x3)
                * (x4 - x3)
                + (intersection_y - y3)
                * (y4 - y3)
            )
            / segment_2_length_squared
        )

        tolerance = 1e-9

        if not (
            -tolerance
            <= parameter_1
            <= 1.0 + tolerance
            and -tolerance
            <= parameter_2
            <= 1.0 + tolerance
        ):
            return None

        return Point(
            intersection_x,
            intersection_y,
            0.0,
        )

    def _grid_point(self, point):
        spacing = self.grid_spacing

        if spacing <= 0:
            return point

        return Point(
            round(point.x / spacing)
            * spacing,
            round(point.y / spacing)
            * spacing,
            point.z,
        )

    # ---------------------------------------------------------
    # CANDIDATOS
    # ---------------------------------------------------------

    def _add_candidate(
        self,
        candidates,
        cursor_point,
        candidate_point,
        snap_type,
    ):
        if not self.mode_enabled(snap_type):
            return

        distance = cursor_point.distance_to(
            candidate_point
        )

        if distance > self.snap_distance:
            return

        priority = self.SNAP_PRIORITY.get(
            snap_type,
            999,
        )

        candidates.append(
            (
                priority,
                distance,
                candidate_point,
                snap_type,
            )
        )

    def _collect_element_candidates(
        self,
        cursor_point,
        scene,
        candidates,
    ):
        for element in scene.get_elements():
            if not self._element_is_visible(
                element,
                scene,
            ):
                continue

            segments = self._element_segments(
                element
            )

            for start, end in segments:
                self._add_candidate(
                    candidates,
                    cursor_point,
                    start,
                    self.MODE_ENDPOINT,
                )

                self._add_candidate(
                    candidates,
                    cursor_point,
                    end,
                    self.MODE_ENDPOINT,
                )

                midpoint = self._midpoint(
                    start,
                    end,
                )

                self._add_candidate(
                    candidates,
                    cursor_point,
                    midpoint,
                    self.MODE_MIDPOINT,
                )

                nearest = (
                    self._nearest_point_on_segment(
                        cursor_point,
                        start,
                        end,
                    )
                )

                self._add_candidate(
                    candidates,
                    cursor_point,
                    nearest,
                    self.MODE_NEAREST,
                )

            if (
                element.__class__.__name__
                == "CadCircle"
            ):
                self._add_candidate(
                    candidates,
                    cursor_point,
                    element.center,
                    self.MODE_CENTER,
                )

                nearest = (
                    self._nearest_point_on_circle(
                        cursor_point,
                        element.center,
                        element.radius,
                    )
                )

                self._add_candidate(
                    candidates,
                    cursor_point,
                    nearest,
                    self.MODE_NEAREST,
                )

    def _collect_intersections(
        self,
        cursor_point,
        scene,
        candidates,
    ):
        if not self.mode_enabled(
            self.MODE_INTERSECTION
        ):
            return

        segments = self._all_segments(
            scene
        )

        for first_index in range(
            len(segments)
        ):
            (
                element_1,
                start_1,
                end_1,
            ) = segments[first_index]

            for second_index in range(
                first_index + 1,
                len(segments),
            ):
                (
                    element_2,
                    start_2,
                    end_2,
                ) = segments[second_index]

                # Evita detectar como intersección
                # los vértices internos de una misma entidad.
                if element_1 is element_2:
                    continue

                intersection = (
                    self._segment_intersection(
                        start_1,
                        end_1,
                        start_2,
                        end_2,
                    )
                )

                if intersection is None:
                    continue

                self._add_candidate(
                    candidates,
                    cursor_point,
                    intersection,
                    self.MODE_INTERSECTION,
                )

    # ---------------------------------------------------------
    # API PRINCIPAL
    # ---------------------------------------------------------

    def snap_point(
        self,
        cursor_point,
        scene,
    ):
        if (
            not self.enabled
            or scene is None
        ):
            return cursor_point, None

        candidates = []

        self._collect_element_candidates(
            cursor_point,
            scene,
            candidates,
        )

        self._collect_intersections(
            cursor_point,
            scene,
            candidates,
        )

        grid_point = self._grid_point(
            cursor_point
        )

        self._add_candidate(
            candidates,
            cursor_point,
            grid_point,
            self.MODE_GRID,
        )

        if not candidates:
            return cursor_point, None

        # Primero se ordena por prioridad de OSNAP
        # y luego por distancia real al cursor.
        candidates.sort(
            key=lambda candidate: (
                candidate[0],
                candidate[1],
            )
        )

        (
            _priority,
            _distance,
            snapped_point,
            snap_type,
        ) = candidates[0]

        return (
            Point(
                snapped_point.x,
                snapped_point.y,
                snapped_point.z,
            ),
            snap_type,
        )