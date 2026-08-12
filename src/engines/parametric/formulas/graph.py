from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DependencyEdge:
    source: str
    target: str


class DependencyCycleError(ValueError):
    pass


class ParameterDependencyGraph:
    def __init__(self) -> None:
        self._forward: dict[str, set[str]] = defaultdict(set)
        self._reverse: dict[str, set[str]] = defaultdict(set)
        self.revision = 0

    def add_node(self, node_id: str) -> None:
        if not node_id.strip():
            raise ValueError("node_id no puede estar vacío")
        existed = node_id in self._forward or node_id in self._reverse
        self._forward[node_id]
        self._reverse[node_id]
        if not existed:
            self.revision += 1

    def add_dependency(self, source: str, target: str) -> None:
        if source == target:
            raise DependencyCycleError("Un parámetro no puede depender de sí mismo")
        self.add_node(source)
        self.add_node(target)
        if target in self._forward[source]:
            return
        self._forward[source].add(target)
        self._reverse[target].add(source)
        if self.has_cycle():
            self._forward[source].remove(target)
            self._reverse[target].remove(source)
            raise DependencyCycleError(f"Ciclo detectado: {source} -> {target}")
        self.revision += 1

    def remove_dependency(self, source: str, target: str) -> bool:
        if target not in self._forward.get(source, set()):
            return False
        self._forward[source].remove(target)
        self._reverse[target].remove(source)
        self.revision += 1
        return True

    def dependencies_of(self, target: str) -> tuple[str, ...]:
        return tuple(sorted(self._reverse.get(target, set())))

    def dependents_of(self, source: str) -> tuple[str, ...]:
        return tuple(sorted(self._forward.get(source, set())))

    def transitive_dependents(self, source: str) -> tuple[str, ...]:
        visited: set[str] = set()
        queue = deque(self._forward.get(source, set()))
        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            queue.extend(self._forward.get(node, set()))
        order = self.topological_order()
        return tuple(node for node in order if node in visited)

    def topological_order(self) -> tuple[str, ...]:
        nodes = set(self._forward) | set(self._reverse)
        indegree = {node: len(self._reverse.get(node, set())) for node in nodes}
        queue = deque(sorted(node for node, degree in indegree.items() if degree == 0))
        result: list[str] = []

        while queue:
            node = queue.popleft()
            result.append(node)
            for dependent in sorted(self._forward.get(node, set())):
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    queue.append(dependent)

        if len(result) != len(nodes):
            raise DependencyCycleError("El grafo contiene ciclos")
        return tuple(result)

    def has_cycle(self) -> bool:
        try:
            self.topological_order()
            return False
        except DependencyCycleError:
            return True

    def snapshot(self) -> dict[str, list[str]]:
        return {
            source: sorted(targets)
            for source, targets in sorted(self._forward.items())
        }
