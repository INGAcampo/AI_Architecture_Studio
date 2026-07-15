"""
AI Architecture Studio
Coordinate Parser

Dynamic Input v1
"""

import math
import re

from engines.geometry.point import Point


class CoordinateParseError(Exception):
    pass


class CoordinateParser:

    ABSOLUTE_PATTERN = re.compile(
        r"^\s*(-?\d+(\.\d+)?)\s*,\s*(-?\d+(\.\d+)?)\s*$"
    )

    RELATIVE_PATTERN = re.compile(
        r"^\s*@\s*(-?\d+(\.\d+)?)\s*,\s*(-?\d+(\.\d+)?)\s*$"
    )

    POLAR_PATTERN = re.compile(
        r"^\s*@\s*(\d+(\.\d+)?)\s*<\s*(-?\d+(\.\d+)?)\s*$"
    )

    DISTANCE_PATTERN = re.compile(
        r"^\s*(\d+(\.\d+)?)\s*$"
    )

    @classmethod
    def parse(
        cls,
        text,
        base_point=None,
        direction_point=None,
    ):

        value = text.strip()

        absolute_match = cls.ABSOLUTE_PATTERN.match(
            value
        )

        if absolute_match:

            x = float(
                absolute_match.group(1)
            )

            y = float(
                absolute_match.group(3)
            )

            return Point(
                x,
                y,
                0.0,
            )

        relative_match = cls.RELATIVE_PATTERN.match(
            value
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
                relative_match.group(3)
            )

            return Point(
                base_point.x + dx,
                base_point.y + dy,
                0.0,
            )

        polar_match = cls.POLAR_PATTERN.match(
            value
        )

        if polar_match:

            if base_point is None:
                raise CoordinateParseError(
                    "No existe punto base."
                )

            distance = float(
                polar_match.group(1)
            )

            angle_deg = float(
                polar_match.group(3)
            )

            angle_rad = math.radians(
                angle_deg
            )

            return Point(
                base_point.x
                + distance * math.cos(angle_rad),

                base_point.y
                + distance * math.sin(angle_rad),

                0.0,
            )

        distance_match = cls.DISTANCE_PATTERN.match(
            value
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

            dx = (
                direction_point.x
                - base_point.x
            )

            dy = (
                direction_point.y
                - base_point.y
            )

            length = math.sqrt(
                dx * dx
                + dy * dy
            )

            if length <= 1e-9:
                raise CoordinateParseError(
                    "Dirección inválida."
                )

            ux = dx / length
            uy = dy / length

            return Point(
                base_point.x
                + ux * distance,

                base_point.y
                + uy * distance,

                0.0,
            )

        raise CoordinateParseError(
            f"Formato inválido: {text}"
        )