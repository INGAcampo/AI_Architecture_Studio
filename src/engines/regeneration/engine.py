from __future__ import annotations

from typing import Any

from .dirty import DirtyTracker
from .model import (
    RegenerationItem,
    RegenerationResult,
    RegenerationStatus,
)
from .queue import RegenerationQueue
from .scheduler import DependencyScheduler
from .transaction import TransactionOperation
from .transaction_manager import TransactionManager


class RegenerationEngine:
    def __init__(
        self,
        *,
        event_dispatcher=None,
        transaction_manager: TransactionManager | None = None,
    ) -> None:
        self.items: dict[str, RegenerationItem] = {}
        self.dirty = DirtyTracker()
        self.queue = RegenerationQueue()
        self.scheduler = DependencyScheduler()
        self.transactions = transaction_manager or TransactionManager()
        self.event_dispatcher = event_dispatcher

    def register(self, item: RegenerationItem, *, replace: bool = False) -> None:
        if item.object_id in self.items and not replace:
            raise KeyError(f"Elemento ya registrado: {item.object_id}")
        self.items[item.object_id] = item
        self.mark_dirty(item.object_id)
        self._publish("regeneration.item.registered", object_id=item.object_id)

    def unregister(self, object_id: str) -> RegenerationItem:
        try:
            item = self.items.pop(object_id)
        except KeyError as exc:
            raise KeyError(f"Elemento desconocido: {object_id}") from exc
        self.dirty.mark_clean(object_id)
        self.queue.remove(object_id)
        self._publish("regeneration.item.unregistered", object_id=object_id)
        return item

    def mark_dirty(self, object_id: str) -> None:
        item = self.require(object_id)
        self.dirty.mark_dirty(object_id)
        item.status = RegenerationStatus.DIRTY
        self.queue.enqueue(item)
        self._publish("regeneration.item.dirty", object_id=object_id)

    def require(self, object_id: str) -> RegenerationItem:
        try:
            return self.items[object_id]
        except KeyError as exc:
            raise KeyError(f"Elemento desconocido: {object_id}") from exc

    def regenerate(self, object_ids: tuple[str, ...] | None = None) -> tuple[RegenerationResult, ...]:
        selected = (
            tuple(self.require(object_id) for object_id in object_ids)
            if object_ids is not None
            else tuple(
                self.require(object_id)
                for object_id in self.dirty.all()
            )
        )
        ordered = self.scheduler.order(selected)
        results: list[RegenerationResult] = []

        with self.transactions.transaction("Regeneración"):
            for item in ordered:
                results.append(self._run_item(item))

        self._publish(
            "regeneration.completed",
            count=len(results),
            success=all(result.success for result in results),
        )
        return tuple(results)

    def _run_item(self, item: RegenerationItem) -> RegenerationResult:
        item.status = RegenerationStatus.RUNNING
        self._publish("regeneration.item.started", object_id=item.object_id)

        previous_revision = item.revision
        previous_status = item.status
        try:
            value = item.callback()
            item.revision += 1
            item.status = RegenerationStatus.COMPLETED
            item.error = None
            self.dirty.mark_clean(item.object_id)
            self.queue.remove(item.object_id)

            self.transactions.add_operation(
                TransactionOperation(
                    redo=lambda: None,
                    undo=lambda i=item, r=previous_revision: self._restore_item(i, r),
                    label=f"Regenerar {item.object_id}",
                )
            )

            result = RegenerationResult(
                item.object_id,
                True,
                value=value,
                revision=item.revision,
            )
            self._publish(
                "regeneration.item.completed",
                object_id=item.object_id,
                revision=item.revision,
            )
            return result
        except Exception as exc:
            item.status = RegenerationStatus.FAILED
            item.error = str(exc)
            self._publish(
                "regeneration.item.failed",
                object_id=item.object_id,
                error=str(exc),
            )
            raise

    def _restore_item(self, item: RegenerationItem, revision: int) -> None:
        item.revision = revision
        item.status = RegenerationStatus.ROLLED_BACK
        self.dirty.mark_dirty(item.object_id)

    def _publish(self, name: str, **payload: Any) -> None:
        target = self.event_dispatcher
        if target is None:
            return
        if callable(target):
            target(name, payload)
            return
        dispatch = getattr(target, "dispatch", None)
        if callable(dispatch):
            try:
                dispatch(name, payload)
            except TypeError:
                dispatch({"name": name, "payload": payload})
