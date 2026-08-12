from __future__ import annotations

from typing import Any, Iterable

from .adapter import PropertySelectionAdapter
from .history import PropertyEditAction
from .model import PropertyPaletteModel


class PropertyPaletteController:
    def __init__(
        self,
        model: PropertyPaletteModel,
        adapter: PropertySelectionAdapter,
        *,
        history_manager=None,
        event_dispatcher=None,
    ) -> None:
        self.model = model
        self.adapter = adapter
        self.history_manager = history_manager
        self.event_dispatcher = event_dispatcher
        self._selection: tuple[Any, ...] = ()

    @property
    def selection(self) -> tuple[Any, ...]:
        return self._selection

    def set_selection(self, objects: Iterable[Any]) -> None:
        self._selection = tuple(objects)
        self.model.set_entries(self.adapter.build_entries(self._selection))
        self._publish(
            "property_palette.selection.changed",
            count=len(self._selection),
            revision=self.model.revision,
        )

    def clear_selection(self) -> None:
        self._selection = ()
        self.model.clear()
        self._publish(
            "property_palette.selection.changed",
            count=0,
            revision=self.model.revision,
        )

    def edit_property(self, property_id: str, value: Any):
        if not self._selection:
            raise RuntimeError("No hay objetos seleccionados")

        normalized_entry = self.model.update_value(property_id, value)
        normalized_value = normalized_entry.value
        action = PropertyEditAction.create(
            self._selection,
            property_id,
            normalized_value,
            label=f"Editar {normalized_entry.descriptor.label}",
        )

        self._execute_action(action)
        self.model.set_entries(self.adapter.build_entries(self._selection))
        self._publish(
            "property_palette.property.changed",
            property_id=property_id,
            value=normalized_value,
            object_count=len(self._selection),
            revision=self.model.revision,
        )
        return self.model.require(property_id)

    def refresh(self) -> None:
        self.model.set_entries(self.adapter.build_entries(self._selection))
        self._publish(
            "property_palette.refreshed",
            revision=self.model.revision,
        )

    def _execute_action(self, action: PropertyEditAction) -> None:
        history = self.history_manager
        if history is None:
            action.redo()
            return

        for method_name in ("execute", "do", "push"):
            method = getattr(history, method_name, None)
            if callable(method):
                method(action)
                return

        action.redo()

    def _publish(self, name: str, **payload) -> None:
        target = self.event_dispatcher
        if target is None:
            return

        dispatch = getattr(target, "dispatch", None)
        if callable(dispatch):
            try:
                dispatch(name, payload)
            except TypeError:
                dispatch({"name": name, "payload": payload})
            return

        emit = getattr(target, "emit", None)
        if callable(emit):
            emit(name, payload)
            return

        if callable(target):
            target(name, payload)
