"""
AI Architecture Studio
Coordinate Parser Professional

Dynamic Input - Package 1

Formatos compatibles:
    12.5        -> distancia directa según la dirección del cursor
    10,25       -> coordenada cartesiana absoluta
    @10,5       -> coordenada cartesiana relativa
    @10<45      -> coordenada polar relativa
    10<45       -> coordenada polar absoluta desde el origen
"""

import math
import re

from engines.geometry.point import Point


class CoordinateParseError(Exception):
    """Error producido al interpretar una entrada de coordenadas."""


class CoordinateParser:
    """
    Convierte texto de Dynamic Input o Command Line en objetos Point.
    """

    NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)"

    ABSOLUTE_PATTERN = re.compile(
        rf"^\s*({NUMBER})\s*,\s*({NUMBER})\s*$"
    )

    RELATIVE_PATTERN = re.compile(
        rf"^\s*@\s*({NUMBER})\s*,\s*({NUMBER})\s*$"
    )

    RELATIVE_POLAR_PATTERN = re.compile(
        rf"^\s*@\s*({NUMBER})\s*<\s*({NUMBER})\s*$"
    )

    ABSOLUTE_POLAR_PATTERN = re.compile(
        rf"^\s*({NUMBER})\s*<\s*({NUMBER})\s*$"
    )

    # Alias conservado para no romper código existente.
    POLAR_PATTERN = RELATIVE_POLAR_PATTERN

    DISTANCE_PATTERN = re.compile(
        rf"^\s*({NUMBER})\s*$"
    )

    @staticmethod
    def _polar_point(origin, distance, angle_degrees):
        """
        Calcula un punto polar desde un origen.
        """
        if distance < 0.0:
            raise CoordinateParseError(
                "La distancia polar no puede ser negativa."
            )

        angle_radians = math.radians(
            angle_degrees
        )

        return Point(
            origin.x
            + distance * math.cos(
                angle_radians
            ),
            origin.y
            + distance * math.sin(
                angle_radians
            ),
            origin.z,
        )

    @classmethod
    def parse(
        cls,
        text,
        base_point=None,
        direction_point=None,
    ):
        """
        Interpreta una entrada CAD y devuelve un Point.

        Orden de evaluación:
            1. Cartesiana relativa: @x,y
            2. Polar relativa: @distancia<ángulo
            3. Cartesiana absoluta: x,y
            4. Polar absoluta: distancia<ángulo
            5. Distancia directa
        """
        value = str(text).strip().replace(";", ",")

        if not value:
            raise CoordinateParseError(
                "La entrada está vacía."
            )

        relative_match = (
            cls.RELATIVE_PATTERN.fullmatch(
                value
            )
        )

        if relative_match:
            if base_point is None:
                raise CoordinateParseError(
                    "No existe punto base."
                )

            dx = float(
                relative_match.group(1)
            )
            dy = float(
                relative_match.group(2)
            )

            return Point(
                base_point.x + dx,
                base_point.y + dy,
                base_point.z,
            )

        relative_polar_match = (
            cls.RELATIVE_POLAR_PATTERN.fullmatch(
                value
            )
        )

        if relative_polar_match:
            if base_point is None:
                raise CoordinateParseError(
                    "No existe punto base."
                )

            distance = float(
                relative_polar_match.group(1)
            )
            angle_degrees = float(
                relative_polar_match.group(2)
            )

            return cls._polar_point(
                base_point,
                distance,
                angle_degrees,
            )

        absolute_match = (
            cls.ABSOLUTE_PATTERN.fullmatch(
                value
            )
        )

        if absolute_match:
            x = float(
                absolute_match.group(1)
            )
            y = float(
                absolute_match.group(2)
            )

            return Point(
                x,
                y,
                0.0,
            )

        absolute_polar_match = (
            cls.ABSOLUTE_POLAR_PATTERN.fullmatch(
                value
            )
        )

        if absolute_polar_match:
            distance = float(
                absolute_polar_match.group(1)
            )
            angle_degrees = float(
                absolute_polar_match.group(2)
            )

            return cls._polar_point(
                Point(0.0, 0.0, 0.0),
                distance,
                angle_degrees,
            )

        distance_match = (
            cls.DISTANCE_PATTERN.fullmatch(
                value
            )
        )

        if distance_match:
            if base_point is None:
                raise CoordinateParseError(
                    "No existe punto base."
                )

            if direction_point is None:
                raise CoordinateParseError(
                    "No existe dirección."
                )

            distance = float(
                distance_match.group(1)
            )

            if distance < 0.0:
                raise CoordinateParseError(
                    "La distancia no puede ser negativa."
                )

            dx = (
                direction_point.x
                - base_point.x
            )
            dy = (
                direction_point.y
                - base_point.y
            )

            length = math.hypot(
                dx,
                dy,
            )

            if length <= 1e-9:
                raise CoordinateParseError(
                    "Dirección inválida."
                )

            unit_x = dx / length
            unit_y = dy / length

            return Point(
                base_point.x
                + unit_x * distance,
                base_point.y
                + unit_y * distance,
                base_point.z,
            )

        raise CoordinateParseError(
            "Formato inválido. Use: distancia, x,y, "
            "@x,y, @distancia<ángulo o distancia<ángulo."
        )
