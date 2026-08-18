"""Núcleo determinista del AIAS Live Data Graph."""

from __future__ import annotations

from collections import deque
from collections.abc import Callable, Iterator
from typing import Any

from .exceptions import (
    DependencyCycleError,
    DuplicateNodeError,
    NodeNotFoundError,
)
from .model import DataNode, GraphChange, NodeState

ChangeListener = Callable[[GraphChange], None]


class LiveDataGraph:
    """Grafo dirigido de dependencias para datos CAD/BIM de AIAS.

    Una arista ``source -> dependent`` significa que el segundo nodo debe
    invalidarse cuando cambia el primero.
    """

    def __init__(self) -> None:
        self._nodes: dict[str, DataNode] = {}
        self._dependents: dict[str, set[str]] = {}
        self._dependencies: dict[str, set[str]] = {}
        self._listeners: list[ChangeListener] = []
        self._revision = 0

    @property
    def revision(self) -> int:
        return self._revision

    def __len__(self) -> int:
        return len(self._nodes)

    def __contains__(self, node_id: object) -> bool:
        return self._key(node_id) in self._nodes

    def __iter__(self) -> Iterator[DataNode]:
        for node_id in sorted(self._nodes):
            yield self._nodes[node_id]

    def add_node(
        self,
        node_id: str,
        kind: str,
        payload: Any = None,
        *,
        metadata: dict[str, Any] | None = None,
        replace: bool = False,
    ) -> DataNode:
        key = self._key(node_id)
        if key in self._nodes and not replace:
            raise DuplicateNodeError(node_id)
        node = DataNode(
            node_id=str(node_id).strip(),
            kind=kind,
            payload=payload,
            metadata=dict(metadata or {}),
        )
        self._nodes[key] = node
        self._dependents.setdefault(key, set())
        self._dependencies.setdefault(key, set())
        return node

    def require_node(self, node_id: str) -> DataNode:
        try:
            return self._nodes[self._key(node_id)]
        except KeyError as exc:
            raise NodeNotFoundError(node_id) from exc

    def remove_node(self, node_id: str) -> DataNode:
        key = self._key(node_id)
        node = self.require_node(node_id)
        for dependency in tuple(self._dependencies.get(key, ())):
            self._dependents[dependency].discard(key)
        for dependent in tuple(self._dependents.get(key, ())):
            self._dependencies[dependent].discard(key)
        self._dependencies.pop(key, None)
        self._dependents.pop(key, None)
        self._nodes.pop(key)
        return node

    def add_dependency(self, source_id: str, dependent_id: str) -> None:
        source = self._key(source_id)
        dependent = self._key(dependent_id)
        self.require_node(source_id)
        self.require_node(dependent_id)
        if source == dependent or self._reachable(dependent, source):
            raise DependencyCycleError(
                f"La dependencia {source_id!r} -> {dependent_id!r} crea un ciclo."
            )
        self._dependents[source].add(dependent)
        self._dependencies[dependent].add(source)

    def remove_dependency(self, source_id: str, dependent_id: str) -> bool:
        source = self._key(source_id)
        dependent = self._key(dependent_id)
        removed = dependent in self._dependents.get(source, set())
        self._dependents.get(source, set()).discard(dependent)
        self._dependencies.get(dependent, set()).discard(source)
        return removed

    def dependencies_of(self, node_id: str) -> tuple[DataNode, ...]:
        key = self._key(node_id)
        self.require_node(node_id)
        return tuple(
            self._nodes[item]
            for item in sorted(self._dependencies[key])
        )

    def dependents_of(
        self,
        node_id: str,
        *,
        recursive: bool = False,
    ) -> tuple[DataNode, ...]:
        key = self._key(node_id)
        self.require_node(node_id)
        ids = (
            self._affected_order(key)[1:]
            if recursive
            else sorted(self._dependents[key])
        )
        return tuple(self._nodes[item] for item in ids)

    def update_payload(
        self,
        node_id: str,
        payload: Any,
        *,
        reason: str = "update",
        metadata: dict[str, Any] | None = None,
    ) -> GraphChange:
        node = self.require_node(node_id)
        node.payload = payload
        return self.mark_dirty(
            node_id,
            reason=reason,
            metadata=metadata,
        )

    def mark_dirty(
        self,
        node_id: str,
        *,
        reason: str = "update",
        metadata: dict[str, Any] | None = None,
    ) -> GraphChange:
        source_key = self._key(node_id)
        self.require_node(node_id)
        ordered = self._affected_order(source_key)
        self._revision += 1
        for key in ordered:
            node = self._nodes[key]
            node.state = NodeState.DIRTY
            node.revision = self._revision
        change = GraphChange(
            source_id=self._nodes[source_key].node_id,
            affected_ids=tuple(self._nodes[key].node_id for key in ordered),
            revision=self._revision,
            reason=str(reason),
            metadata=metadata or {},
        )
        for listener in tuple(self._listeners):
            listener(change)
        return change

    def mark_clean(self, node_id: str, *, recursive: bool = False) -> None:
        key = self._key(node_id)
        self.require_node(node_id)
        ids = self._affected_order(key) if recursive else (key,)
        for item in ids:
            self._nodes[item].state = NodeState.CLEAN

    def subscribe(self, listener: ChangeListener) -> Callable[[], None]:
        if listener not in self._listeners:
            self._listeners.append(listener)

        def unsubscribe() -> None:
            try:
                self._listeners.remove(listener)
            except ValueError:
                pass

        return unsubscribe

    def snapshot(self) -> dict[str, dict[str, Any]]:
        return {
            node.node_id: {
                "kind": node.kind,
                "state": node.state.value,
                "revision": node.revision,
                "metadata": dict(node.metadata),
            }
            for node in self
        }

    def _affected_order(self, source: str) -> tuple[str, ...]:
        ordered: list[str] = []
        visited: set[str] = set()
        queue: deque[str] = deque((source,))
        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            ordered.append(current)
            queue.extend(
                item
                for item in sorted(self._dependents[current])
                if item not in visited
            )
        return tuple(ordered)

    def _reachable(self, start: str, target: str) -> bool:
        queue: deque[str] = deque((start,))
        visited: set[str] = set()
        while queue:
            current = queue.popleft()
            if current == target:
                return True
            if current in visited:
                continue
            visited.add(current)
            queue.extend(self._dependents.get(current, ()))
        return False

    @staticmethod
    def _key(value: object) -> str:
        return str(value).strip().casefold()
