from __future__ import annotations
from dataclasses import dataclass, field, replace
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class AssistantContext:
    project: Any = None
    active_document_id: str | None = None
    active_level_id: str | None = None
    discipline: str | None = None
    selected_element_ids: tuple[str, ...] = ()
    user_id: str | None = None
    settings: Mapping[str, Any] = field(default_factory=dict)


class ContextManager:
    def __init__(self, context: AssistantContext | None = None) -> None:
        self._context = context or AssistantContext()

    def get(self) -> AssistantContext:
        return self._context

    def update(self, **changes: Any) -> AssistantContext:
        self._context = replace(self._context, **changes)
        return self._context

    def clear_selection(self) -> AssistantContext:
        return self.update(selected_element_ids=())

    def set_selection(self, element_ids) -> AssistantContext:
        return self.update(selected_element_ids=tuple(str(x) for x in element_ids))

    def snapshot(self) -> dict[str, Any]:
        context = self._context
        return {
            "active_document_id": context.active_document_id,
            "active_level_id": context.active_level_id,
            "discipline": context.discipline,
            "selected_element_ids": context.selected_element_ids,
            "user_id": context.user_id,
            "settings": dict(context.settings),
        }
