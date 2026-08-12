from __future__ import annotations

from typing import Any, Iterable

from .collection import ParameterCollection
from .registry import ParameterDefinitionRegistry
from .types import ParameterChange, ParameterDefinition
from .validator import ParameterValidator


class ParameterEngine:
    def __init__(
        self,
        registry: ParameterDefinitionRegistry | None = None,
        *,
        validator: ParameterValidator | None = None,
        event_dispatcher=None,
    ) -> None:
        self.registry = registry or ParameterDefinitionRegistry()
        self.validator = validator or ParameterValidator()
        self.event_dispatcher = event_dispatcher
        self._collections: dict[str, ParameterCollection] = {}

    def create_collection(
        self,
        owner_id: str,
        definitions: Iterable[ParameterDefinition] | None = None,
    ) -> ParameterCollection:
        if owner_id in self._collections:
            raise KeyError(f"Ya existe una colección para {owner_id}")
        collection = ParameterCollection(owner_id, validator=self.validator)
        for definition in definitions or ():
            collection.add_definition(definition)
        self._collections[owner_id] = collection
        self._publish("parameter.collection.created", owner_id=owner_id)
        return collection

    def get_collection(self, owner_id: str) -> ParameterCollection:
        try:
            return self._collections[owner_id]
        except KeyError as exc:
            raise KeyError(f"Colección desconocida: {owner_id}") from exc

    def remove_collection(self, owner_id: str) -> ParameterCollection:
        collection = self.get_collection(owner_id)
        self._collections.pop(owner_id)
        self._publish("parameter.collection.removed", owner_id=owner_id)
        return collection

    def set_value(
        self,
        owner_id: str,
        parameter_id: str,
        value: Any,
        *,
        source: str = "user",
    ) -> ParameterChange | None:
        collection = self.get_collection(owner_id)
        before = collection.value(parameter_id)
        result = collection.set(parameter_id, value, source=source)
        if before == result.value:
            return None
        change = ParameterChange(
            owner_id=owner_id,
            parameter_id=parameter_id,
            old_value=before,
            new_value=result.value,
            revision=result.revision,
            source=source,
        )
        self._publish(
            "parameter.changed",
            owner_id=owner_id,
            parameter_id=parameter_id,
            old_value=before,
            new_value=result.value,
            revision=result.revision,
            source=source,
        )
        return change

    def set_calculated(
        self,
        owner_id: str,
        parameter_id: str,
        value: Any,
        *,
        source: str = "formula",
    ) -> ParameterChange | None:
        collection = self.get_collection(owner_id)
        before = collection.value(parameter_id)
        result = collection.set_calculated(parameter_id, value, source=source)
        if before == result.value:
            return None
        change = ParameterChange(
            owner_id,
            parameter_id,
            before,
            result.value,
            result.revision,
            source,
        )
        self._publish(
            "parameter.calculated",
            owner_id=owner_id,
            parameter_id=parameter_id,
            value=result.value,
            revision=result.revision,
        )
        return change

    def _publish(self, name: str, **payload) -> None:
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
