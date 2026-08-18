"""
AI Architecture Studio
CAD Polyline Object

Package 4.1.1 — FILLET PLINE
Compatible con polilíneas clásicas por puntos y polilíneas
híbridas formadas por segmentos LINE / ARC.
"""

from engines.geometry.point import Point
from engines.geometry.line import Line
from models.base_object import BaseObject


class CadPolyline(BaseObject):

    def __init__(self):
        super().__init__(
            name="Polilínea CAD",
            object_type="CadPolyline",
        )

        self.points = []
        self.segments = []
        self.closed = False

    @staticmethod
    def _copy_point(point):
        return Point(point.x, point.y, point.z)

    def _rebuild_linear_segments(self):
        """
        Mantiene compatibilidad con la implementación histórica.
        Se ejecuta mientras la entidad no contiene arcos.
        """
        if any(
            segment.__class__.__name__ == "CadArc"
            for segment in self.segments
        ):
            return

        self.segments = []

        if len(self.points) < 2:
            return

        for index in range(len(self.points) - 1):
            self.segments.append(
                Line(
                    self._copy_point(self.points[index]),
                    self._copy_point(self.points[index + 1]),
                )
            )

        if self.closed and len(self.points) > 2:
            self.segments.append(
                Line(
                    self._copy_point(self.points[-1]),
                    self._copy_point(self.points[0]),
                )
            )

    def add_point(self, point):
        self.points.append(point)
        self._rebuild_linear_segments()

    def add_segment(self, segment):
        self.segments.append(segment)
        self._sync_points_from_segments()

    def set_segments(self, segments, closed=None):
        self.segments = list(segments)

        if closed is not None:
            self.closed = bool(closed)

        self._sync_points_from_segments()

    def _segment_start(self, segment):
        if segment.__class__.__name__ == "Line":
            return segment.start

        return getattr(segment, "start_point", None)

    def _segment_end(self, segment):
        if segment.__class__.__name__ == "Line":
            return segment.end

        return getattr(segment, "end_point", None)

    def _sync_points_from_segments(self):
        """
        points continúa disponible para selección, grips y módulos
        antiguos. En segmentos con arco conserva los extremos.
        """
        if not self.segments:
            return

        points = []
        first = self._segment_start(self.segments[0])

        if first is not None:
            points.append(self._copy_point(first))

        for segment in self.segments:
            end = self._segment_end(segment)

            if end is not None:
                points.append(self._copy_point(end))

        if (
            self.closed
            and len(points) > 1
            and points[-1].distance_to(points[0]) <= 1.0e-9
        ):
            points.pop()

        self.points = points

    def close(self):
        self.closed = True
        self._rebuild_linear_segments()

    @property
    def segment_count(self):
        if self.segments:
            return len(self.segments)

        if len(self.points) < 2:
            return 0

        return len(self.points) if self.closed else len(self.points) - 1

    def get_segments(self):
        if not self.segments:
            self._rebuild_linear_segments()

        return list(self.segments)

    def clone(self):
        from models.cad_arc import CadArc

        cloned = CadPolyline()
        cloned.closed = self.closed

        if self.segments:
            copied = []

            for segment in self.segments:
                kind = segment.__class__.__name__

                if kind == "Line":
                    copied.append(
                        Line(
                            self._copy_point(segment.start),
                            self._copy_point(segment.end),
                        )
                    )
                elif kind == "CadArc":
                    copied.append(segment.clone())

            cloned.set_segments(copied, closed=self.closed)
            return cloned

        for point in self.points:
            cloned.points.append(self._copy_point(point))

        cloned._rebuild_linear_segments()
        return cloned

    def info(self):
        data = super().info()
        data["Puntos"] = len(self.points)
        data["Segmentos"] = self.segment_count
        data["Cerrada"] = self.closed
        data["Segmentos mixtos"] = any(
            segment.__class__.__name__ == "CadArc"
            for segment in self.segments
        )
        return data
