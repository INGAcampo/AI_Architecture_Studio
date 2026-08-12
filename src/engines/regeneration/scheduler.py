from __future__ import annotations

from collections import defaultdict, deque

from .model import RegenerationItem


class RegenerationDependencyCycleError(ValueError):
    pass


class DependencyScheduler:
    def order(
        self,
        items: tuple[RegenerationItem, ...],
    ) -> tuple[RegenerationItem, ...]:
        by_id = {item.object_id: item for item in items}
        forward: dict[str, set[str]] = defaultdict(set)
        indegree = {item.object_id: 0 for item in items}

        for item in items:
            for dependency in item.dependencies:
                if dependency not in by_id:
                    continue
                forward[dependency].add(item.object_id)
                indegree[item.object_id] += 1

        queue = deque(
            sorted(
                (object_id for object_id, degree in indegree.items() if degree == 0),
                key=lambda object_id: (
                    by_id[object_id].priority,
                    object_id,
                ),
            )
        )
        result: list[RegenerationItem] = []

        while queue:
            object_id = queue.popleft()
            result.append(by_id[object_id])
            for dependent in sorted(forward.get(object_id, ())):
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    queue.append(dependent)

        if len(result) != len(items):
            raise RegenerationDependencyCycleError(
                "Se detectó un ciclo de regeneración"
            )
        return tuple(result)
