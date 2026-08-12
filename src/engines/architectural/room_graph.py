"""Grafo planar de WALL para detección de caras cerradas."""

import math

from engines.architectural.wall_network import WallNetwork
from engines.geometry.point import Point


class RoomGraph:
    EPSILON = 1.0e-8

    def __init__(self, tolerance=1.0e-5):
        self.tolerance = float(tolerance)
        self.points = {}
        self.adjacency = {}
        self.edges = set()

    def _key(self, point):
        scale = 1.0 / max(self.tolerance, self.EPSILON)
        return (
            int(round(point.x * scale)),
            int(round(point.y * scale)),
        )

    def _point(self, point):
        key = self._key(point)
        if key not in self.points:
            self.points[key] = Point(
                point.x,
                point.y,
                getattr(point, "z", 0.0),
            )
            self.adjacency[key] = set()
        return key

    def add_edge(self, first, second):
        first_key = self._point(first)
        second_key = self._point(second)
        if first_key == second_key:
            return

        edge = tuple(sorted((first_key, second_key)))
        if edge in self.edges:
            return

        self.edges.add(edge)
        self.adjacency[first_key].add(second_key)
        self.adjacency[second_key].add(first_key)

    @classmethod
    def from_scene(cls, scene, tolerance=1.0e-5):
        graph = cls(tolerance=tolerance)
        network = WallNetwork.ensure_scene(scene, tolerance=tolerance)

        for wall in network.walls:
            path = list(getattr(wall, "path", []) or [])
            connections = list(
                getattr(wall, "wall_connections", []) or []
            )

            by_segment = {}
            for connection in connections:
                index = int(connection.get("segment_index", -1))
                parameter = float(connection.get("parameter", 0.0))
                position = connection.get("position")
                if index < 0 or position is None:
                    continue
                by_segment.setdefault(index, []).append(
                    (parameter, position)
                )

            for index in range(len(path) - 1):
                first = path[index]
                second = path[index + 1]
                candidates = [
                    (0.0, first),
                    (1.0, second),
                ]
                candidates.extend(by_segment.get(index, []))
                candidates.sort(key=lambda item: item[0])

                unique = []
                for parameter, point in candidates:
                    if unique and abs(parameter - unique[-1][0]) <= tolerance:
                        continue
                    unique.append((parameter, point))

                for position in range(len(unique) - 1):
                    graph.add_edge(
                        unique[position][1],
                        unique[position + 1][1],
                    )

        return graph

    def _sorted_neighbors(self):
        result = {}
        for node, neighbors in self.adjacency.items():
            origin = self.points[node]
            result[node] = sorted(
                neighbors,
                key=lambda neighbor: math.atan2(
                    self.points[neighbor].y - origin.y,
                    self.points[neighbor].x - origin.x,
                ),
            )
        return result

    @staticmethod
    def signed_area(points):
        if len(points) < 3:
            return 0.0
        return 0.5 * sum(
            points[index].x * points[(index + 1) % len(points)].y
            - points[(index + 1) % len(points)].x * points[index].y
            for index in range(len(points))
        )

    @staticmethod
    def _canonical_cycle(keys):
        sequence = list(keys)
        if sequence and sequence[0] == sequence[-1]:
            sequence.pop()
        if not sequence:
            return tuple()

        variants = []
        for candidate in (sequence, list(reversed(sequence))):
            for offset in range(len(candidate)):
                variants.append(
                    tuple(candidate[offset:] + candidate[:offset])
                )
        return min(variants)

    def faces(self, minimum_area=1.0e-5):
        """Enumera las caras interiores del grafo planar.

        Se recorre cada media arista dejando la cara a la izquierda.
        Las caras interiores resultan antihorarias (área positiva).
        """
        ordered = self._sorted_neighbors()
        visited = set()
        faces = []
        known = set()
        max_steps = max(16, len(self.edges) * 4 + 8)

        for first, neighbors in ordered.items():
            for second in neighbors:
                half_edge = (first, second)
                if half_edge in visited:
                    continue

                cycle = []
                current = half_edge

                for _ in range(max_steps):
                    if current in visited:
                        break

                    visited.add(current)
                    start, end = current
                    cycle.append(start)

                    around_end = ordered.get(end, [])
                    if start not in around_end or len(around_end) < 2:
                        cycle = []
                        break

                    incoming_index = around_end.index(start)
                    next_node = around_end[
                        (incoming_index - 1) % len(around_end)
                    ]
                    current = (end, next_node)

                    if current == half_edge:
                        break
                else:
                    cycle = []

                if len(cycle) < 3 or current != half_edge:
                    continue

                canonical = self._canonical_cycle(cycle)
                if canonical in known:
                    continue

                polygon = [self.points[key] for key in cycle]
                area = self.signed_area(polygon)

                if area <= minimum_area:
                    continue

                known.add(canonical)
                faces.append(polygon)

        return faces
