"""Stable JSON serialization and reconstruction for supported geometry primitives."""
from __future__ import annotations
import json
from pathlib import Path
from .primitives import Point2D, Line2D, Circle2D
from .polygon import Polygon2D

class GeometrySerializer:
    """Preserve type identity and numeric coordinates across JSON boundaries."""
    def to_dict(self, obj):
        """Convert a supported geometry object into a tagged primitive mapping."""
        if isinstance(obj, Point2D):
            return {"type":"Point2D","x":obj.x,"y":obj.y}
        if isinstance(obj, Line2D):
            return {"type":"Line2D","start":self.to_dict(obj.start),"end":self.to_dict(obj.end)}
        if isinstance(obj, Circle2D):
            return {"type":"Circle2D","center":self.to_dict(obj.center),"radius":obj.radius}
        if isinstance(obj, Polygon2D):
            return {"type":"Polygon2D","vertices":[self.to_dict(p) for p in obj.vertices]}
        raise TypeError(type(obj).__name__)

    def from_dict(self, data):
        """Reconstruct a supported geometry object from its tagged mapping."""
        t = data["type"]
        if t=="Point2D":
            return Point2D(data["x"],data["y"])
        if t=="Line2D":
            return Line2D(self.from_dict(data["start"]),self.from_dict(data["end"]))
        if t=="Circle2D":
            return Circle2D(self.from_dict(data["center"]),data["radius"])
        if t=="Polygon2D":
            return Polygon2D(tuple(self.from_dict(p) for p in data["vertices"]))
        raise ValueError("unsupported_geometry_type")

    def save(self, obj, path: Path):
        """Persist a supported geometry object as readable JSON."""
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(self.to_dict(obj),indent=2),encoding="utf-8")
        return path
