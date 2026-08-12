"""AI Architecture Studio
Architectural Core 5.0.5.2.1 — DOOR History Fix.

Puerta paramétrica con identidad persistente para Undo/Redo seguro.
"""

from uuid import uuid4


class Door:
    LEFT = "left"
    RIGHT = "right"

    INWARD = "inward"
    OUTWARD = "outward"

    SINGLE = "single"

    def __init__(
        self,
        opening=None,
        width=0.90,
        height=2.10,
        handedness=LEFT,
        swing_direction=INWARD,
        door_type=SINGLE,
        name="Puerta",
        door_id=None,
    ):
        self.door_id = str(door_id or uuid4())
        self.opening = opening
        self.width = float(width)
        self.height = float(height)
        self.handedness = str(handedness)
        self.swing_direction = str(swing_direction)
        self.door_type = str(door_type)
        self.name = str(name)
        self.visible = True
        self.validate()

    @property
    def id(self):
        return self.door_id

    def validate(self):
        if self.width <= 0.0:
            raise ValueError(
                "El ancho de la puerta debe ser mayor que cero."
            )
        if self.height <= 0.0:
            raise ValueError(
                "La altura de la puerta debe ser mayor que cero."
            )
        if self.handedness not in (
            self.LEFT,
            self.RIGHT,
        ):
            raise ValueError(
                "Sentido de puerta inválido."
            )
        if self.swing_direction not in (
            self.INWARD,
            self.OUTWARD,
        ):
            raise ValueError(
                "Dirección de apertura inválida."
            )

    @property
    def host_wall(self):
        if self.opening is None:
            return None
        return self.opening.host_wall

    @property
    def center_point(self):
        if self.opening is None:
            return None
        return self.opening.center_point

    def flip_handedness(self):
        self.handedness = (
            self.RIGHT
            if self.handedness == self.LEFT
            else self.LEFT
        )
        return self.handedness

    def flip_swing_direction(self):
        self.swing_direction = (
            self.OUTWARD
            if self.swing_direction == self.INWARD
            else self.INWARD
        )
        return self.swing_direction

    def clone(
        self,
        opening=None,
        preserve_id=False,
    ):
        return Door(
            opening=(
                opening
                if opening is not None
                else self.opening
            ),
            width=self.width,
            height=self.height,
            handedness=self.handedness,
            swing_direction=self.swing_direction,
            door_type=self.door_type,
            name=self.name,
            door_id=(
                self.door_id
                if preserve_id
                else None
            ),
        )

    def as_dict(self):
        return {
            "door_id": self.door_id,
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "handedness": self.handedness,
            "swing_direction": self.swing_direction,
            "door_type": self.door_type,
        }
