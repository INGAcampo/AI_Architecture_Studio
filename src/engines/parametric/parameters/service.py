from __future__ import annotations

from typing import Any, Iterable

from .engine import ParameterEngine
from .history import ParameterEditAction
from .types import ParameterDefinition


class ParameterService:
    def __init__(
        self,
        engine: ParameterEngine | None = None,
        *,
        history_manager=None,
    ) -> None:
        self.engine = engine or ParameterEngine()
        self.history_manager = history_manager

    def create_owner(
        self,
        owner_id: str,
        definitions: Iterable[ParameterDefinition],
    ):
        return self.engine.create_collection(owner_id, definitions)

    def edit(
        self,
        owner_id: str,
        parameter_id: str,
        value: Any,
    ):
        collection = self.engine.get_collection(owner_id)
        before = collection.value(parameter_id)
        normalized = collection.validator.normalize(
            collection.get(parameter_id).definition,
            value,
        )
        if before == normalized:
            return None

        action = ParameterEditAction(
            self.engine,
            owner_id,
            parameter_id,
            before,
            normalized,
            label=f"Editar {parameter_id}",
        )

        history = self.history_manager
        if history is None:
            action.redo()
        else:
            for method_name in ("execute", "do", "push"):
                method = getattr(history, method_name, None)
                if callable(method):
                    method(action)
                    break
            else:
                action.redo()

        return action
