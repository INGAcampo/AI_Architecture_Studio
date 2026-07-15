"""
AI Architecture Studio
Grip Editor

Professional Grips v1 - Package 4A
"""

from engines.geometry.point import Point


class GripEditor:
    def __init__(self):
        self.grip = None
        self.owner = None
        self.start_point = None
        self.original_state = None
        self.dragging = False

    def begin(self, grip):
        if grip is None:
            return False

        owner = getattr(grip, "owner", None)

        if owner is None or owner.__class__.__name__ != "CadLine":
            return False

        self.grip = grip
        self.owner = owner
        self.start_point = self._copy_point(grip.point)
        self.original_state = self.capture_state(owner)
        self.dragging = True
        grip.activate()
        return True

    def update(self, point):
        if not self.dragging or point is None:
            return False

        geometry = self.owner.geometry
        grip_type = self.grip.grip_type
        grip_index = self.grip.index

        if grip_type == "endpoint" and grip_index == 0:
            geometry.start = self._copy_point(point)

        elif grip_type == "endpoint" and grip_index == 1:
            geometry.end = self._copy_point(point)

        elif grip_type == "midpoint":
            dx = point.x - self.start_point.x
            dy = point.y - self.start_point.y
            dz = point.z - self.start_point.z

            start = self.original_state["start"]
            end = self.original_state["end"]

            geometry.start = Point(
                start.x + dx,
                start.y + dy,
                start.z + dz,
            )
            geometry.end = Point(
                end.x + dx,
                end.y + dy,
                end.z + dz,
            )
        else:
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

        self.grip.deactivate()
        self._reset()
        return result

    def cancel(self):
        if self.owner is not None and self.original_state is not None:
            self.apply_state(self.owner, self.original_state)

        if self.grip is not None:
            self.grip.deactivate()

        self._reset()

    def _reset(self):
        self.grip = None
        self.owner = None
        self.start_point = None
        self.original_state = None
        self.dragging = False

    @classmethod
    def capture_state(cls, owner):
        geometry = owner.geometry

        return {
            "type": "CadLine",
            "start": cls._copy_point(geometry.start),
            "end": cls._copy_point(geometry.end),
        }

    @classmethod
    def apply_state(cls, owner, state):
        if (
            owner.__class__.__name__ != "CadLine"
            or state.get("type") != "CadLine"
        ):
            return False

        owner.geometry.start = cls._copy_point(state["start"])
        owner.geometry.end = cls._copy_point(state["end"])
        return True

    @staticmethod
    def _copy_point(point):
        return Point(point.x, point.y, point.z)