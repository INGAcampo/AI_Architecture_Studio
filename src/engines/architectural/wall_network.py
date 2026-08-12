"""AIAS WALL Network Engine — Architectural Core 5.0.4.3.

Construye una topología persistente durante la sesión a partir de los
objetos Wall presentes en la escena. Detecta extremos, encuentros L/T/X
e intersecciones entre segmentos.
"""

import math

from engines.geometry.point import Point
from models.architectural.wall_node import WallNode


class WallNetwork:
    EPSILON = 1.0e-8
    DEFAULT_TOLERANCE = 1.0e-5

    def __init__(self, tolerance=DEFAULT_TOLERANCE):
        self.tolerance = float(tolerance)
        self.nodes = []
        self.walls = []
        self.revision = 0

    @staticmethod
    def _cross(ax, ay, bx, by):
        return ax * by - ay * bx

    @staticmethod
    def _distance(a, b):
        return math.hypot(a.x - b.x, a.y - b.y)

    @classmethod
    def _segment_intersection(cls, a, b, c, d, tolerance):
        """Devuelve (Point, t, u) para segmentos AB y CD o None."""
        rx = b.x - a.x
        ry = b.y - a.y
        sx = d.x - c.x
        sy = d.y - c.y
        denominator = cls._cross(rx, ry, sx, sy)
        qpx = c.x - a.x
        qpy = c.y - a.y

        if abs(denominator) <= tolerance:
            # Paralelos/colineales: registramos extremos coincidentes.
            candidates = (
                (a, 0.0, cls._parameter_on_segment(a, c, d)),
                (b, 1.0, cls._parameter_on_segment(b, c, d)),
                (c, cls._parameter_on_segment(c, a, b), 0.0),
                (d, cls._parameter_on_segment(d, a, b), 1.0),
            )
            for point, t, u in candidates:
                if t is None or u is None:
                    continue
                if cls._distance_to_segment(point, a, b) <= tolerance and cls._distance_to_segment(point, c, d) <= tolerance:
                    return Point(point.x, point.y, getattr(point, "z", 0.0)), t, u
            return None

        t = cls._cross(qpx, qpy, sx, sy) / denominator
        u = cls._cross(qpx, qpy, rx, ry) / denominator

        if -tolerance <= t <= 1.0 + tolerance and -tolerance <= u <= 1.0 + tolerance:
            t = min(1.0, max(0.0, t))
            u = min(1.0, max(0.0, u))
            return (
                Point(a.x + t * rx, a.y + t * ry, getattr(a, "z", 0.0)),
                t,
                u,
            )
        return None

    @staticmethod
    def _parameter_on_segment(point, a, b):
        dx = b.x - a.x
        dy = b.y - a.y
        denominator = dx * dx + dy * dy
        if denominator <= 1.0e-18:
            return None
        return ((point.x - a.x) * dx + (point.y - a.y) * dy) / denominator

    @classmethod
    def _distance_to_segment(cls, point, a, b):
        t = cls._parameter_on_segment(point, a, b)
        if t is None:
            return cls._distance(point, a)
        t = min(1.0, max(0.0, t))
        projection = Point(a.x + (b.x - a.x) * t, a.y + (b.y - a.y) * t, 0.0)
        return cls._distance(point, projection)

    def _find_or_create_node(self, point):
        for node in self.nodes:
            if self._distance(node.position, point) <= self.tolerance:
                return node
        node = WallNode(f"WN-{len(self.nodes) + 1:04d}", point)
        self.nodes.append(node)
        return node

    @staticmethod
    def _is_endpoint_parameter(value, tolerance):
        return value <= tolerance or value >= 1.0 - tolerance

    @staticmethod
    def _wall_segments(wall):
        path = list(getattr(wall, "path", []) or [])
        return [(path[i], path[i + 1], i) for i in range(len(path) - 1)]

    def _register_connection(self, node, wall, segment_index, parameter):
        endpoint = self._is_endpoint_parameter(parameter, self.tolerance)
        node.add_connection(wall, segment_index, parameter, endpoint)

    def _classify_node(self, node):
        wall_count = len(node.connected_walls)
        endpoint_count = sum(1 for item in node.connections if item["endpoint"])
        interior_count = node.degree - endpoint_count

        # Dos segmentos que atraviesan el mismo punto generan una X,
        # aunque pertenezcan solamente a dos objetos Wall.
        if interior_count >= 2 or wall_count >= 4 or node.degree >= 4:
            return WallNode.X_JOIN

        # Un extremo que llega al interior de otro segmento genera una T.
        if (interior_count >= 1 and endpoint_count >= 1) or wall_count >= 3:
            return WallNode.T_JOIN

        # Dos extremos coincidentes o un vértice de una polilínea generan L.
        if wall_count >= 2 or node.degree >= 2:
            return WallNode.L_JOIN
        return WallNode.ENDPOINT

    def rebuild(self, walls):
        self.nodes = []
        self.walls = [
            wall for wall in (walls or [])
            if wall.__class__.__name__ == "Wall"
        ]

        # Registrar extremos de todos los segmentos.
        for wall in self.walls:
            for a, b, segment_index in self._wall_segments(wall):
                node_a = self._find_or_create_node(a)
                node_b = self._find_or_create_node(b)
                self._register_connection(node_a, wall, segment_index, 0.0)
                self._register_connection(node_b, wall, segment_index, 1.0)

        # Registrar intersecciones entre paredes diferentes y entre
        # segmentos no adyacentes de una misma pared.
        entries = []
        for wall in self.walls:
            for a, b, segment_index in self._wall_segments(wall):
                entries.append((wall, segment_index, a, b))

        for index, first in enumerate(entries):
            wall_a, segment_a, a, b = first
            for wall_b, segment_b, c, d in entries[index + 1:]:
                if wall_a is wall_b and abs(segment_a - segment_b) <= 1:
                    continue
                result = self._segment_intersection(a, b, c, d, self.tolerance)
                if result is None:
                    continue
                point, t, u = result
                node = self._find_or_create_node(point)
                self._register_connection(node, wall_a, segment_a, t)
                self._register_connection(node, wall_b, segment_b, u)

        for node in self.nodes:
            node.node_type = self._classify_node(node)

        # Persistir referencias topológicas en cada Wall.
        for wall in self.walls:
            wall.wall_network_revision = self.revision + 1
            wall.wall_node_ids = []
            wall.wall_connections = []

        for node in self.nodes:
            for connection in node.connections:
                wall = connection["wall"]
                if node.node_id not in wall.wall_node_ids:
                    wall.wall_node_ids.append(node.node_id)
                wall.wall_connections.append(
                    {
                        "node_id": node.node_id,
                        "node_type": node.node_type,
                        "segment_index": connection["segment_index"],
                        "parameter": connection["parameter"],
                        "endpoint": connection["endpoint"],
                        "position": Point(
                            node.position.x,
                            node.position.y,
                            node.position.z,
                        ),
                    }
                )
            updater = getattr(node, "as_dict", None)
            if callable(updater):
                updater()

        for wall in self.walls:
            rebuild = getattr(wall, "rebuild_wall_geometry", None)
            if callable(rebuild):
                rebuild()
            update = getattr(wall, "_update_properties", None)
            if callable(update):
                update()

        self.revision += 1
        return self


    @staticmethod
    def _scene_signature(elements):
        signature = []
        for wall in elements or []:
            if wall.__class__.__name__ != "Wall":
                continue
            path_signature = tuple(
                (round(point.x, 9), round(point.y, 9), round(getattr(point, "z", 0.0), 9))
                for point in (getattr(wall, "path", []) or [])
            )
            signature.append(
                (
                    id(wall),
                    path_signature,
                    round(float(getattr(wall, "thickness", 0.0)), 9),
                    bool(getattr(wall, "visible", True)),
                )
            )
        return tuple(signature)

    @classmethod
    def ensure_scene(cls, scene, tolerance=DEFAULT_TOLERANCE):
        """Reconstruye la red solo cuando cambian los muros de la escena."""
        if scene is None:
            return cls(tolerance=tolerance)

        getter = getattr(scene, "get_elements", None)
        elements = getter() if callable(getter) else []
        signature = cls._scene_signature(elements)
        current = getattr(scene, "wall_network", None)

        if (
            isinstance(current, cls)
            and getattr(scene, "wall_network_signature", None) == signature
        ):
            return current

        network = cls(tolerance=tolerance).rebuild(elements)
        scene.wall_network = network
        scene.wall_network_signature = signature
        return network

    @classmethod
    def from_scene(cls, scene, tolerance=DEFAULT_TOLERANCE):
        network = cls(tolerance=tolerance)
        if scene is None:
            return network
        getter = getattr(scene, "get_elements", None)
        elements = getter() if callable(getter) else []
        return network.rebuild(elements)

    def summary(self):
        counts = {
            WallNode.ENDPOINT: 0,
            WallNode.L_JOIN: 0,
            WallNode.T_JOIN: 0,
            WallNode.X_JOIN: 0,
        }
        for node in self.nodes:
            counts[node.node_type] = counts.get(node.node_type, 0) + 1
        return {
            "walls": len(self.walls),
            "nodes": len(self.nodes),
            "L": counts.get(WallNode.L_JOIN, 0),
            "T": counts.get(WallNode.T_JOIN, 0),
            "X": counts.get(WallNode.X_JOIN, 0),
            "revision": self.revision,
        }

    def get_node(self, node_id):
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        return None

    def nearest_node(self, point, tolerance=0.35):
        best = None
        best_distance = float(tolerance)
        for node in self.nodes:
            distance = self._distance(node.position, point)
            if distance <= best_distance:
                best = node
                best_distance = distance
        return best
