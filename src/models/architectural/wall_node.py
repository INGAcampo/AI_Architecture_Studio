"""AIAS Architectural Wall Node — WALL NETWORK 5.0.4.3."""

from engines.geometry.point import Point


class WallNode:
    """Nodo topológico compartido entre uno o varios muros."""

    ENDPOINT = "ENDPOINT"
    L_JOIN = "L"
    T_JOIN = "T"
    X_JOIN = "X"
    INTERSECTION = "INTERSECTION"

    def __init__(self, node_id, position, node_type=ENDPOINT):
        self.node_id = str(node_id)
        self.position = Point(
            position.x,
            position.y,
            getattr(position, "z", 0.0),
        )
        self.node_type = str(node_type)
        self.connections = []

    def add_connection(self, wall, segment_index, parameter, endpoint=False):
        for item in self.connections:
            if (
                item["wall"] is wall
                and item["segment_index"] == int(segment_index)
                and abs(item["parameter"] - float(parameter)) <= 1.0e-9
            ):
                return

        self.connections.append(
            {
                "wall": wall,
                "segment_index": int(segment_index),
                "parameter": float(parameter),
                "endpoint": bool(endpoint),
            }
        )

    @property
    def degree(self):
        return len(self.connections)

    @property
    def connected_walls(self):
        result = []
        for item in self.connections:
            wall = item["wall"]
            if wall not in result:
                result.append(wall)
        return result

    def as_dict(self):
        return {
            "node_id": self.node_id,
            "x": self.position.x,
            "y": self.position.y,
            "z": self.position.z,
            "node_type": self.node_type,
            "degree": self.degree,
            "wall_count": len(self.connected_walls),
        }
