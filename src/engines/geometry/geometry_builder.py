"""
AI Architecture Studio
Geometry Builder

Foundation 2.6
"""

from engines.geometry.point import Point
from engines.geometry.line import Line

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
        Construye un rectángulo utilizando una polilínea.
        """

        x1 = first_corner.x
        y1 = first_corner.y

        x2 = second_corner.x
        y2 = second_corner.y

        poly = CadPolyline()

        poly.add_point(Point(x1, y1, 0))
        poly.add_point(Point(x2, y1, 0))
        poly.add_point(Point(x2, y2, 0))
        poly.add_point(Point(x1, y2, 0))

        poly.close()

        return CadRectangle(poly)