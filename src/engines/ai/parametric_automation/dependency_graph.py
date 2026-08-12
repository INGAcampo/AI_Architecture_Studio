from __future__ import annotations
from collections import defaultdict, deque


class DependencyCycleError(ValueError):
    pass


class DependencyGraph:
    def __init__(self) -> None:
        self._dependencies: dict[str, set[str]] = defaultdict(set)
        self._dependents: dict[str, set[str]] = defaultdict(set)

    def add_node(self, node_id: str) -> None:
        if not node_id.strip():
            raise ValueError("node_id es obligatorio")
        self._dependencies.setdefault(node_id, set())
        self._dependents.setdefault(node_id, set())

    def add_dependency(self, node_id: str, depends_on: str) -> None:
        self.add_node(node_id)
        self.add_node(depends_on)
        self._dependencies[node_id].add(depends_on)
        self._dependents[depends_on].add(node_id)
        if self.has_cycle():
            self._dependencies[node_id].remove(depends_on)
            self._dependents[depends_on].remove(node_id)
            raise DependencyCycleError(
                f"La dependencia {node_id} -> {depends_on} crea un ciclo"
            )

    def dependencies_of(self, node_id: str) -> tuple[str, ...]:
        return tuple(sorted(self._dependencies.get(node_id, ())))

    def dependents_of(self, node_id: str) -> tuple[str, ...]:
        return tuple(sorted(self._dependents.get(node_id, ())))

    def has_cycle(self) -> bool:
        try:
            self.topological_order()
        except DependencyCycleError:
            return True
        return False

    def topological_order(self) -> tuple[str, ...]:
        indegree = {
            node: len(dependencies)
            for node, dependencies in self._dependencies.items()
        }
        queue = deque(
            sorted(node for node, degree in indegree.items() if degree == 0)
        )
        order = []

        while queue:
            node = queue.popleft()
            order.append(node)
            for dependent in sorted(self._dependents.get(node, ())):
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    queue.append(dependent)

        if len(order) != len(indegree):
            raise DependencyCycleError("El grafo contiene un ciclo")
        return tuple(order)

    def affected_by(self, node_id: str) -> tuple[str, ...]:
        visited = set()
        queue = deque(self._dependents.get(node_id, ()))

        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            queue.extend(self._dependents.get(node, ()))

        order = self.topological_order()
        return tuple(node for node in order if node in visited)
