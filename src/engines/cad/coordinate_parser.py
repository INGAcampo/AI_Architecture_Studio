"""
AI Architecture Studio
Coordinate Parser Professional

Versión corregida para soporte de punto y coma decimal.

Formatos soportados:

    12.5
    12,5

    10,25
    10.25;5.75

    @10,5
    @10.25;5.75

    @10<45
    @10.5<45

    10<45
"""

import math
import re

from engines.geometry.point import Point


class CoordinateParseError(Exception):
    """Error producido al interpretar una entrada."""


class CoordinateParser:

    NUMBER = r"[+-]?(?:\d+(?:[\.,]\d*)?|[\.,]\d+)"

    ABSOLUTE_PATTERN = re.compile(
        rf"^\s*({NUMBER})\s*[,;]\s*({NUMBER})\s*$"
    )

    RELATIVE_PATTERN = re.compile(
        rf"^\s*@\s*({NUMBER})\s*[,;]\s*({NUMBER})\s*$"
    )

    RELATIVE_POLAR_PATTERN = re.compile(
        rf"^\s*@\s*({NUMBER})\s*<\s*({NUMBER})\s*$"
    )

    ABSOLUTE_POLAR_PATTERN = re.compile(
        rf"^\s*({NUMBER})\s*<\s*({NUMBER})\s*$"
    )

    POLAR_PATTERN = RELATIVE_POLAR_PATTERN

    DISTANCE_PATTERN = re.compile(
        rf"^\s*({NUMBER})\s*$"
    )

    @staticmethod
    def _to_float(value):
        return float(
            str(value).replace(",", ".")
        )

    @staticmethod
    def _polar_point(origin, distance, angle_degrees):

        if distance < 0.0:
            raise CoordinateParseError(
                "La distancia polar no puede ser negativa."
            )

        angle_radians = math.radians(
            angle_degrees
        )

        return Point(
            origin.x + distance * math.cos(angle_radians),
            origin.y + distance * math.sin(angle_radians),
            origin.z,
        )

    @classmethod
    def parse(
        cls,
        text,
        base_point=None,
        direction_point=None,
    ):

        value = str(text).strip()

        if not value:
            raise CoordinateParseError(
                "La entrada está vacía."
            )

        match = cls.RELATIVE_PATTERN.fullmatch(value)

        if match:

            if base_point is None:
                raise CoordinateParseError(
                    "No existe punto base."
                )

            dx = cls._to_float(match.group(1))
            dy = cls._to_float(match.group(2))

            return Point(
                base_point.x + dx,
                base_point.y + dy,
                base_point.z,
            )

        match = cls.RELATIVE_POLAR_PATTERN.fullmatch(value)

        if match:

            if base_point is None:
                raise CoordinateParseError(
                    "No existe punto base."
                )

            return cls._polar_point(
                base_point,
                cls._to_float(match.group(1)),
                cls._to_float(match.group(2)),
            )

        match = cls.ABSOLUTE_PATTERN.fullmatch(value)

        if match:

            return Point(
                cls._to_float(match.group(1)),
                cls._to_float(match.group(2)),
                0.0,
            )

        match = cls.ABSOLUTE_POLAR_PATTERN.fullmatch(value)

        if match:

            return cls._polar_point(
                Point(0.0, 0.0, 0.0),
                cls._to_float(match.group(1)),
                cls._to_float(match.group(2)),
            )

        match = cls.DISTANCE_PATTERN.fullmatch(value)

        if match:

            if base_point is None:
                raise CoordinateParseError(
                    "No existe punto base."
                )

            if direction_point is None:
                raise CoordinateParseError(
                    "No existe dirección."
                )

            distance = cls._to_float(
                match.group(1)
            )

            dx = direction_point.x - base_point.x
            dy = direction_point.y - base_point.y

            length = math.hypot(dx, dy)

            if length <= 1e-9:
                raise CoordinateParseError(
                    "Dirección inválida."
                )

            return Point(
                base_point.x + dx / length * distance,
                base_point.y + dy / length * distance,
                base_point.z,
            )

        raise CoordinateParseError(
            "Formato inválido."
        )