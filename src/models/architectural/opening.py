"""AI Architecture Studio
Architectural Core 5.0.5.2.1 — Opening model.

Hueco paramétrico con identidad persistente y alojamiento único.
"""

from uuid import uuid4

from engines.geometry.point import Point


class WallOpening:
    GENERIC = "Opening"
    DOOR = "Door"
    WINDOW = "Window"

    def __init__(
        self,
        host_wall=None,
        segment_index=0,
        parameter=0.5,
        width=0.90,
        height=2.10,
        sill_height=0.0,
        opening_type=GENERIC,
        name="Hueco",
        opening_id=None,
    ):
        self.opening_id = str(
            opening_id or uuid4()
        )
        self.host_wall = host_wall
        self.segment_index = int(segment_index)
        self.parameter = float(parameter)
        self.width = float(width)
        self.height = float(height)
        self.sill_height = float(sill_height)
        self.opening_type = str(opening_type)
        self.name = str(name)
        self.visible = True

        self.door = None
        self.window = None

        self.validate()

    @property
    def id(self):
        return self.opening_id

    def validate(self):
        if self.width <= 0.0:
            raise ValueError(
                "El ancho del hueco debe ser mayor que cero."
            )
        if self.height <= 0.0:
            raise ValueError(
                "La altura del hueco debe ser mayor que cero."
            )
        if self.sill_height < 0.0:
            raise ValueError(
                "El antepecho no puede ser negativo."
            )
        self.parameter = min(
            1.0,
            max(0.0, self.parameter),
        )
        self.segment_index = max(
            0,
            self.segment_index,
        )

    @property
    def center_point(self):
        wall = self.host_wall
        path = list(
            getattr(wall, "path", []) or []
        )

        if len(path) < 2:
            return Point(0.0, 0.0, 0.0)

        index = min(
            self.segment_index,
            len(path) - 2,
        )
        first = path[index]
        second = path[index + 1]
        parameter = min(
            1.0,
            max(0.0, self.parameter),
        )

        return Point(
            first.x
            + (second.x - first.x) * parameter,
            first.y
            + (second.y - first.y) * parameter,
            getattr(first, "z", 0.0)
            + (
                getattr(second, "z", 0.0)
                - getattr(first, "z", 0.0)
            )
            * parameter,
        )

    @property
    def hosted_element(self):
        return self.door or self.window

    def attach_door(self, door):
        if door is None:
            raise ValueError(
                "No se puede alojar una puerta vacía."
            )

        current = self.door
        current_id = getattr(
            current,
            "door_id",
            None,
        )
        incoming_id = getattr(
            door,
            "door_id",
            None,
        )

        if (
            current is not None
            and current is not door
            and current_id != incoming_id
        ):
            current.opening = None

        self.door = door
        self.window = None
        self.opening_type = self.DOOR
        self.name = "Hueco de puerta"
        door.opening = self
        self.width = door.width
        self.height = door.height
        self.sill_height = 0.0
        return door

    def detach_door(self):
        door = self.door
        self.door = None

        if door is not None:
            door.opening = self

        if self.window is None:
            self.opening_type = self.GENERIC
            self.name = "Hueco"

        return door

    def attach_window(self, window):
        if window is None:
            raise ValueError("No se puede alojar una ventana vacía.")
        self.window = window
        self.door = None
        self.opening_type = self.WINDOW
        self.name = "Hueco de ventana"
        window.opening = self
        self.width = window.width
        self.height = window.height
        self.sill_height = window.sill_height
        return window

    def detach_window(self):
        window = self.window
        self.window = None
        if window is not None:
            window.opening = self
        if self.door is None:
            self.opening_type = self.GENERIC
            self.name = "Hueco"
        return window

    def clone(
        self,
        host_wall=None,
        preserve_id=False,
    ):
        clone = WallOpening(
            host_wall=(
                host_wall
                if host_wall is not None
                else self.host_wall
            ),
            segment_index=self.segment_index,
            parameter=self.parameter,
            width=self.width,
            height=self.height,
            sill_height=self.sill_height,
            opening_type=self.opening_type,
            name=self.name,
            opening_id=(
                self.opening_id
                if preserve_id
                else None
            ),
        )

        if self.door is not None:
            clone.attach_door(
                self.door.clone(
                    opening=clone,
                    preserve_id=preserve_id,
                )
            )
        if self.window is not None:
            clone.attach_window(
                self.window.clone(opening=clone,preserve_id=preserve_id)
            )
        return clone

    def as_dict(self):
        center = self.center_point

        return {
            "opening_id": self.opening_id,
            "name": self.name,
            "type": self.opening_type,
            "segment_index": self.segment_index,
            "parameter": self.parameter,
            "width": self.width,
            "height": self.height,
            "sill_height": self.sill_height,
            "center": Point(
                center.x,
                center.y,
                center.z,
            ),
            "door": (
                self.door.as_dict()
                if self.door is not None
                else None
            ),
        }
