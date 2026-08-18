from __future__ import annotations

from .model import Point2D


def polygon_area(points: tuple[Point2D, ...]) -> float:
    if len(points) < 3:
        raise ValueError("Se requieren al menos tres puntos")
    total = 0.0
    for index, current in enumerate(points):
        nxt = points[(index + 1) % len(points)]
        total += current.x * nxt.y - nxt.x * current.y
    return abs(total) * 0.5


def polygon_perimeter(points: tuple[Point2D, ...]) -> float:
    if len(points) < 2:
        return 0.0
    total = 0.0
    for index, current in enumerate(points):
        nxt = points[(index + 1) % len(points)]
        total += ((nxt.x - current.x) ** 2 + (nxt.y - current.y) ** 2) ** 0.5
    return total


def is_clockwise(points: tuple[Point2D, ...]) -> bool:
    signed = 0.0
    for index, current in enumerate(points):
        nxt = points[(index + 1) % len(points)]
        signed += (nxt.x - current.x) * (nxt.y + current.y)
    return signed > 0


def point_in_polygon(point: Point2D, polygon: tuple[Point2D, ...]) -> bool:
    inside = False
    j = len(polygon) - 1
    for i in range(len(polygon)):
        pi = polygon[i]
        pj = polygon[j]
        intersects = (
            (pi.y > point.y) != (pj.y > point.y)
            and point.x
            < (pj.x - pi.x) * (point.y - pi.y) / ((pj.y - pi.y) or 1e-12) + pi.x
        )
        if intersects:
            inside = not inside
        j = i
    return inside
