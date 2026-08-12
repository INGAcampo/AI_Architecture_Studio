"""Homogeneous two-dimensional translation, rotation, scaling and composition."""
from __future__ import annotations
import math
from dataclasses import dataclass
from .primitives import Point2D

@dataclass(frozen=True, slots=True)
class Transform2D:
    """Apply and compose affine transforms without mutating source geometry."""
    m00: float = 1.0
    m01: float = 0.0
    m02: float = 0.0
    m10: float = 0.0
    m11: float = 1.0
    m12: float = 0.0

    def apply(self, p: Point2D) -> Point2D:
        """Apply the affine matrix to a planar point."""
        return Point2D(
            self.m00*p.x + self.m01*p.y + self.m02,
            self.m10*p.x + self.m11*p.y + self.m12,
        )

    @classmethod
    def translation(cls, dx: float, dy: float) -> "Transform2D":
        """Construct a translation transform from x and y offsets."""
        return cls(m02=dx,m12=dy)

    @classmethod
    def scale(cls, sx: float, sy: float | None = None) -> "Transform2D":
        """Construct uniform or independent-axis scaling about the origin."""
        sy = sx if sy is None else sy
        return cls(m00=sx,m11=sy)

    @classmethod
    def rotation(cls, radians: float) -> "Transform2D":
        """Construct a counterclockwise rotation about the origin."""
        c, s = math.cos(radians), math.sin(radians)
        return cls(c,-s,0,s,c,0)

    def compose(self, other: "Transform2D") -> "Transform2D":
        """Return a transform applying another transform followed by this one."""
        return Transform2D(
            self.m00*other.m00+self.m01*other.m10,
            self.m00*other.m01+self.m01*other.m11,
            self.m00*other.m02+self.m01*other.m12+self.m02,
            self.m10*other.m00+self.m11*other.m10,
            self.m10*other.m01+self.m11*other.m11,
            self.m10*other.m02+self.m11*other.m12+self.m12,
        )
