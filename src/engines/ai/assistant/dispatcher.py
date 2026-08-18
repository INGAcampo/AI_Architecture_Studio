from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Mapping

from .action import ActionStatus, AssistantAction
from .context_manager import ContextManager


@dataclass(frozen=True, slots=True)
class DispatchResult:
    action: AssistantAction
    status: ActionStatus
    value: Any = None
    error: str | None = None


class ActionDispatcher:
    def __init__(
        self,
        context_manager: ContextManager,
        *,
        services: Mapping[str, Any] | None = None,
    ) -> None:
        self.context_manager = context_manager
        self.services = dict(services or {})
        self._handlers: dict[str, Callable[[AssistantAction], Any]] = {
            "query_selection": self._query_selection,
            "query_counts": self._query_counts,
            "query_issues": self._query_issues,
            "query_context": self._query_context,
            "modify_property": self._modify_property,
            "run_rules": self._run_rules,
        }

    def register_handler(self, action_type: str, handler: Callable[[AssistantAction], Any]) -> None:
        self._handlers[action_type] = handler

    def dispatch(self, action: AssistantAction) -> DispatchResult:
        handler = self._handlers.get(action.action_type)
        if handler is None:
            return DispatchResult(
                action=action,
                status=ActionStatus.FAILED,
                error=f"Acción no soportada: {action.action_type}",
            )
        try:
            value = handler(action)
        except Exception as exc:
            return DispatchResult(
                action=action,
                status=ActionStatus.FAILED,
                error=str(exc),
            )
        return DispatchResult(
            action=action,
            status=ActionStatus.COMPLETED,
            value=value,
        )

    def _query_selection(self, action: AssistantAction):
        return self.context_manager.get().selected_element_ids

    def _query_context(self, action: AssistantAction):
        return self.context_manager.snapshot()

    def _query_counts(self, action: AssistantAction):
        project = self.context_manager.get().project
        elements = ()
        if isinstance(project, dict):
            elements = tuple(project.get("elements", ()))
        else:
            elements = tuple(getattr(project, "elements", ())) if project is not None else ()

        entity = str(action.payload.get("entity", "elements")).lower()
        singular_map = {
            "columnas": "column",
            "puertas": "door",
            "muros": "wall",
            "vigas": "beam",
            "losas": "slab",
        }
        if entity == "elements":
            return len(elements)
        expected = singular_map.get(entity, entity.rstrip("s"))
        count = 0
        for element in elements:
            kind = element.get("kind") if isinstance(element, dict) else getattr(element, "kind", None)
            if str(kind).lower() == expected:
                count += 1
        return count

    def _query_issues(self, action: AssistantAction):
        rule_engine = self.services.get("rule_engine")
        if rule_engine is None:
            return ()
        return rule_engine.issues()

    def _run_rules(self, action: AssistantAction):
        rule_engine = self.services.get("rule_engine")
        if rule_engine is None:
            raise RuntimeError("Rule Engine no disponible")
        return rule_engine.run(self.context_manager.get().project)

    def _modify_property(self, action: AssistantAction):
        selection = self.context_manager.get().selected_element_ids
        if not selection:
            raise RuntimeError("No hay elementos seleccionados")
        property_service = self.services.get("property_service")
        if property_service is None:
            return {
                "element_ids": selection,
                "property": action.payload.get("property"),
                "value": action.payload.get("value"),
                "simulated": True,
            }
        results = []
        for element_id in selection:
            results.append(property_service.set_value(
                element_id,
                action.payload.get("property"),
                action.payload.get("value"),
            ))
        return tuple(results)
