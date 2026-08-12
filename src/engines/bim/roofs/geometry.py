from __future__ import annotations

from math import cos, radians

from .model import RoofPoint


def polygon_area(points: tuple[RoofPoint, ...]) -> float:
    total = 0.0
    for index, current in enumerate(points):
        nxt = points[(index + 1) % len(points)]
        total += current.x * nxt.y - nxt.x * current.y
    return abs(total) * 0.5


def polygon_perimeter(points: tuple[RoofPoint, ...]) -> float:
    total = 0.0
    for index, current in enumerate(points):
        nxt = points[(index + 1) % len(points)]
        total += ((nxt.x - current.x) ** 2 + (nxt.y - current.y) ** 2) ** 0.5
    return total


def sloped_area(projected_area: float, pitch_degrees: float) -> float:
    factor = cos(radians(pitch_degrees))
    if factor <= 0:
        raise ValueError("Pendiente inválida")
    return projected_area / factor


def point_in_polygon(point: RoofPoint, polygon: tuple[RoofPoint, ...]) -> bool:
    inside = False
    j = len(polygon) - 1
    for i in range(len(polygon)):
        pi, pj = polygon[i], polygon[j]
        intersects = (
            (pi.y > point.y) != (pj.y > point.y)
            and point.x < (pj.x - pi.x) * (point.y - pi.y) / ((pj.y - pi.y) or 1e-12) + pi.x
        )
        if intersects:
            inside = not inside
        j = i
    return inside
