from __future__ import annotations
from typing import Any

from .context_manager import ContextManager
from .conversation_memory import ConversationMemory
from .dispatcher import ActionDispatcher, DispatchResult
from .planner import AssistantPlan, Planner
from .prompt_parser import PromptParser
from .response import AssistantResponse, ResponseKind


class AIDesignAssistant:
    def __init__(
        self,
        *,
        context_manager: ContextManager | None = None,
        parser: PromptParser | None = None,
        planner: Planner | None = None,
        dispatcher: ActionDispatcher | None = None,
        memory: ConversationMemory | None = None,
        services: dict[str, Any] | None = None,
    ) -> None:
        self.context_manager = context_manager or ContextManager()
        self.parser = parser or PromptParser()
        self.planner = planner or Planner()
        self.dispatcher = dispatcher or ActionDispatcher(
            self.context_manager,
            services=services,
        )
        self.memory = memory or ConversationMemory()

    def plan(self, prompt: str) -> AssistantPlan:
        intent = self.parser.parse(prompt)
        return self.planner.create_plan(intent)

    def execute(self, plan: AssistantPlan) -> tuple[DispatchResult, ...]:
        return tuple(
            self.dispatcher.dispatch(step.action)
            for step in plan.steps
        )

    def ask(self, prompt: str) -> AssistantResponse:
        self.memory.add("user", prompt)
        plan = self.plan(prompt)
        if plan.is_empty:
            response = AssistantResponse(
                "No pude interpretar la solicitud.",
                ResponseKind.ERROR,
                {"intent": plan.intent.intent_type.value},
            )
            self.memory.add("assistant", response.text)
            return response

        results = self.execute(plan)
        failed = [result for result in results if result.error]
        if failed:
            response = AssistantResponse(
                failed[0].error or "La acción falló.",
                ResponseKind.ERROR,
                {"results": results},
            )
        else:
            response = AssistantResponse(
                self.explain(results),
                ResponseKind.ACTION_RESULT,
                {"results": results},
            )

        self.memory.add("assistant", response.text)
        return response

    def explain(self, results: tuple[DispatchResult, ...]) -> str:
        if not results:
            return "No se ejecutaron acciones."
        if len(results) == 1:
            value = results[0].value
            if isinstance(value, tuple) and value and hasattr(value[0], "to_dict"):
                return f"Se encontraron {len(value)} incidencias."
            if isinstance(value, tuple):
                return f"Resultado: {list(value)}"
            if isinstance(value, dict):
                return f"Resultado: {value}"
            return f"Resultado: {value}"
        return f"Se ejecutaron {len(results)} acciones."

    def history(self):
        return self.memory.all()

    def clear(self) -> None:
        self.memory.clear()

    def context(self):
        return self.context_manager.get()

    def suggestions(self) -> tuple[str, ...]:
        context = self.context_manager.get()
        suggestions = [
            "¿Qué elemento está seleccionado?",
            "¿Cuántas incidencias BIM existen?",
            "Revisa el proyecto.",
        ]
        if context.selected_element_ids:
            suggestions.append("Modifica una propiedad del elemento seleccionado.")
        return tuple(suggestions)
