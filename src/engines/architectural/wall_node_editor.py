"""Editor paramétrico de nodos compartidos WALL 5.0.4.4."""

from engines.geometry.point import Point
from engines.architectural.wall_network import WallNetwork


class WallNodeEditor:
    PICK_TOLERANCE = 0.35

    @staticmethod
    def clone_paths(walls):
        return {
            wall: [Point(p.x, p.y, getattr(p, "z", 0.0)) for p in wall.path]
            for wall in walls
        }

    @staticmethod
    def nearest_node(network, point, tolerance=PICK_TOLERANCE):
        if network is None or point is None:
            return None
        best = None
        best_distance = float(tolerance)
        for node in network.nodes:
            dx = node.position.x - point.x
            dy = node.position.y - point.y
            distance = (dx * dx + dy * dy) ** 0.5
            if distance <= best_distance:
                best = node
                best_distance = distance
        return best

    @staticmethod
    def _replace_endpoint(wall, segment_index, parameter, target):
        index = int(segment_index) if parameter <= 0.5 else int(segment_index) + 1
        if 0 <= index < len(wall.path):
            wall.path[index] = Point(target.x, target.y, getattr(target, "z", 0.0))

    @staticmethod
    def _insert_or_move_interior(wall, segment_index, parameter, target, source_position):
        index = int(segment_index)
        # Si ya hay un vértice coincidente, muévelo en vez de insertar otro.
        for candidate in (index, index + 1):
            if 0 <= candidate < len(wall.path):
                p = wall.path[candidate]
                if ((p.x-source_position.x)**2 + (p.y-source_position.y)**2) ** 0.5 <= 1.0e-6:
                    wall.path[candidate] = Point(target.x, target.y, getattr(target, "z", 0.0))
                    return
        wall.path.insert(index + 1, Point(target.x, target.y, getattr(target, "z", 0.0)))

    @classmethod
    def move_node(cls, scene, node, target):
        if scene is None or node is None or target is None:
            return {}, {}

        affected = list(node.connected_walls)
        before = cls.clone_paths(affected)
        source = Point(node.position.x, node.position.y, node.position.z)

        # Procesar de índice mayor a menor evita desajustes al insertar vértices.
        grouped = {}
        for connection in node.connections:
            grouped.setdefault(connection["wall"], []).append(connection)

        for wall, connections in grouped.items():
            for connection in sorted(connections, key=lambda item: item["segment_index"], reverse=True):
                if connection["endpoint"]:
                    cls._replace_endpoint(
                        wall,
                        connection["segment_index"],
                        connection["parameter"],
                        target,
                    )
                else:
                    cls._insert_or_move_interior(
                        wall,
                        connection["segment_index"],
                        connection["parameter"],
                        target,
                        source,
                    )

            cleaner = getattr(wall, "set_path", None)
            if callable(cleaner):
                cleaner(wall.path)
            else:
                rebuild = getattr(wall, "rebuild_wall_geometry", None)
                if callable(rebuild):
                    rebuild()

        scene.wall_network_signature = None
        WallNetwork.ensure_scene(scene)
        after = cls.clone_paths(affected)
        return before, after
