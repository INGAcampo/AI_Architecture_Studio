"""
AI Architecture Studio
Grip Editor

Professional Grips v5.1
Supports: CadLine, CadPolyline, CadRectangle
"""

from engines.geometry.point import Point


class GripEditor:

    SUPPORTED_TYPES = {
        "CadLine",
        "CadPolyline",
        "CadRectangle",
    }

    def __init__(self):
        self.grip = None
        self.owner = None
        self.start_point = None
        self.original_state = None
        self.dragging = False

    # ---------------------------------------------------------
    # CICLO DE EDICIÓN
    # ---------------------------------------------------------

    def begin(self, grip):
        if grip is None:
            return False

        owner = getattr(grip, "owner", None)

        if (
            owner is None
            or owner.__class__.__name__
            not in self.SUPPORTED_TYPES
        ):
            return False

        original_state = self.capture_state(owner)

        if original_state is None:
            return False

        self.grip = grip
        self.owner = owner
        self.start_point = self._copy_point(grip.point)
        self.original_state = original_state
        self.dragging = True

        grip.activate()
        return True

    def update(self, point):
        if (
            not self.dragging
            or point is None
            or self.owner is None
            or self.grip is None
        ):
            return False

        owner_type = self.owner.__class__.__name__

        if owner_type == "CadLine":
            changed = self._update_line(point)

        elif owner_type == "CadPolyline":
            changed = self._update_polyline(point)

        elif owner_type == "CadRectangle":
            changed = self._update_rectangle(point)

        else:
            changed = False

        if not changed:
            return False

        self.grip.set_point(point)
        return True

    def finish(self):
        if not self.dragging:
            return None

        result = {
            "owner": self.owner,
            "before": self.original_state,
            "after": self.capture_state(self.owner),
        }

        if self.grip is not None:
            self.grip.deactivate()

        self._reset()
        return result

    def cancel(self):
        if (
            self.owner is not None
            and self.original_state is not None
        ):
            self.apply_state(
                self.owner,
                self.original_state,
            )

        if self.grip is not None:
            self.grip.deactivate()

        self._reset()

    def _reset(self):
        self.grip = None
        self.owner = None
        self.start_point = None
        self.original_state = None
        self.dragging = False

    # ---------------------------------------------------------
    # LÍNEA
    # ---------------------------------------------------------

    def _update_line(self, point):
        geometry = getattr(
            self.owner,
            "geometry",
            None,
        )

        if geometry is None:
            return False

        grip_type = getattr(
            self.grip,
            "grip_type",
            "",
        )

        grip_index = getattr(
            self.grip,
            "index",
            None,
        )

        if (
            grip_type == "endpoint"
            and grip_index == 0
        ):
            self._set_point_values(
                geometry.start,
                point,
            )
            return True

        if (
            grip_type == "endpoint"
            and grip_index == 1
        ):
            self._set_point_values(
                geometry.end,
                point,
            )
            return True

        if grip_type == "midpoint":
            dx = point.x - self.start_point.x
            dy = point.y - self.start_point.y
            dz = point.z - self.start_point.z

            original_start = self.original_state["start"]
            original_end = self.original_state["end"]

            self._set_point_values(
                geometry.start,
                Point(
                    original_start.x + dx,
                    original_start.y + dy,
                    original_start.z + dz,
                ),
            )

            self._set_point_values(
                geometry.end,
                Point(
                    original_end.x + dx,
                    original_end.y + dy,
                    original_end.z + dz,
                ),
            )

            return True

        return False

    # ---------------------------------------------------------
    # POLILÍNEA
    # ---------------------------------------------------------

    def _update_polyline(self, point):
        grip_index = getattr(
            self.grip,
            "index",
            None,
        )

        points = getattr(
            self.owner,
            "points",
            None,
        )

        if (
            points is None
            or grip_index is None
            or grip_index < 0
            or grip_index >= len(points)
        ):
            return False

        # Importante: modificar el Point existente.
        # No reemplazar points[index], porque geometry/render
        # pueden conservar referencias al objeto original.
        self._set_point_values(
            points[grip_index],
            point,
        )

        geometry = getattr(
            self.owner,
            "geometry",
            None,
        )

        geometry_points = getattr(
            geometry,
            "points",
            None,
        )

        if (
            geometry_points is not None
            and geometry_points is not points
            and grip_index < len(geometry_points)
        ):
            self._set_point_values(
                geometry_points[grip_index],
                point,
            )

        self._refresh_owner(self.owner)
        return True

    # ---------------------------------------------------------
    # RECTÁNGULO
    # ---------------------------------------------------------

    def _update_rectangle(self, point):
        grip_index = getattr(
            self.grip,
            "index",
            None,
        )

        polyline = getattr(
            self.owner,
            "polyline",
            None,
        )

        if (
            polyline is None
            or grip_index is None
            or len(polyline.points) != 4
            or grip_index < 0
            or grip_index >= 4
        ):
            return False

        original_points = self.original_state["points"]
        corner = original_points[grip_index]

        previous_index = (grip_index - 1) % 4
        next_index = (grip_index + 1) % 4

        previous_point = original_points[previous_index]
        next_point = original_points[next_index]

        updated_points = [
            self._copy_point(value)
            for value in original_points
        ]

        updated_points[grip_index] = self._copy_point(point)

        previous_is_vertical = (
            abs(previous_point.x - corner.x)
            <= abs(previous_point.y - corner.y)
        )

        if previous_is_vertical:
            updated_points[previous_index].x = point.x
            updated_points[next_index].y = point.y
        else:
            updated_points[previous_index].y = point.y
            updated_points[next_index].x = point.x

        # Mantener las mismas instancias Point para que el
        # renderer vea el cambio inmediatamente.
        for index, updated_point in enumerate(
            updated_points
        ):
            self._set_point_values(
                polyline.points[index],
                updated_point,
            )

        polyline.closed = True

        geometry = getattr(
            self.owner,
            "geometry",
            None,
        )

        geometry_points = getattr(
            geometry,
            "points",
            None,
        )

        if (
            geometry_points is not None
            and geometry_points is not polyline.points
            and len(geometry_points) == 4
        ):
            for index, updated_point in enumerate(
                updated_points
            ):
                self._set_point_values(
                    geometry_points[index],
                    updated_point,
                )

        self._refresh_owner(self.owner)
        return True

    # ---------------------------------------------------------
    # ESTADO PARA UNDO / REDO
    # ---------------------------------------------------------

    @classmethod
    def capture_state(cls, owner):
        owner_type = owner.__class__.__name__

        if owner_type == "CadLine":
            geometry = owner.geometry

            return {
                "type": "CadLine",
                "start": cls._copy_point(
                    geometry.start
                ),
                "end": cls._copy_point(
                    geometry.end
                ),
            }

        if owner_type == "CadPolyline":
            return {
                "type": "CadPolyline",
                "points": [
                    cls._copy_point(point)
                    for point in owner.points
                ],
                "closed": bool(owner.closed),
            }

        if owner_type == "CadRectangle":
            return {
                "type": "CadRectangle",
                "points": [
                    cls._copy_point(point)
                    for point in owner.polyline.points
                ],
                "closed": bool(
                    owner.polyline.closed
                ),
            }

        return None

    @classmethod
    def apply_state(
        cls,
        owner,
        state,
    ):
        if not state:
            return False

        owner_type = owner.__class__.__name__
        state_type = state.get("type")

        if (
            owner_type == "CadLine"
            and state_type == "CadLine"
        ):
            cls._set_point_values(
                owner.geometry.start,
                state["start"],
            )
            cls._set_point_values(
                owner.geometry.end,
                state["end"],
            )
            cls._refresh_owner(owner)
            return True

        if (
            owner_type == "CadPolyline"
            and state_type == "CadPolyline"
        ):
            source_points = state["points"]

            if len(owner.points) != len(source_points):
                owner.points = [
                    cls._copy_point(point)
                    for point in source_points
                ]
            else:
                for index, source_point in enumerate(
                    source_points
                ):
                    cls._set_point_values(
                        owner.points[index],
                        source_point,
                    )

            owner.closed = bool(
                state.get("closed", False)
            )

            geometry = getattr(
                owner,
                "geometry",
                None,
            )
            geometry_points = getattr(
                geometry,
                "points",
                None,
            )

            if (
                geometry_points is not None
                and geometry_points is not owner.points
                and len(geometry_points) == len(source_points)
            ):
                for index, source_point in enumerate(
                    source_points
                ):
                    cls._set_point_values(
                        geometry_points[index],
                        source_point,
                    )

            cls._refresh_owner(owner)
            return True

        if (
            owner_type == "CadRectangle"
            and state_type == "CadRectangle"
        ):
            source_points = state["points"]
            polyline = owner.polyline

            if len(polyline.points) != len(source_points):
                polyline.points = [
                    cls._copy_point(point)
                    for point in source_points
                ]
            else:
                for index, source_point in enumerate(
                    source_points
                ):
                    cls._set_point_values(
                        polyline.points[index],
                        source_point,
                    )

            polyline.closed = bool(
                state.get("closed", True)
            )
            owner.geometry = polyline

            cls._refresh_owner(owner)
            return True

        return False

    # ---------------------------------------------------------
    # UTILIDADES
    # ---------------------------------------------------------

    @staticmethod
    def _set_point_values(target, source):
        target.x = source.x
        target.y = source.y
        target.z = source.z

    @staticmethod
    def _copy_point(point):
        return Point(
            point.x,
            point.y,
            point.z,
        )

    @staticmethod
    def _refresh_owner(owner):
        for method_name in (
            "_update_properties",
            "update_properties",
            "refresh_geometry",
            "rebuild_geometry",
        ):
            method = getattr(
                owner,
                method_name,
                None,
            )

            if callable(method):
                method()
                break