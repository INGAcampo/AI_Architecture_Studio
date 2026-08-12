import pytest

from engines.ai.assistant import (
    AIDesignAssistant,
    ActionDispatcher,
    ActionStatus,
    AssistantAction,
    AssistantContext,
    ContextManager,
    ConversationMemory,
    IntentType,
    Planner,
    PromptParser,
)


class FakeRuleEngine:
    def __init__(self):
        self._issues = ("issue-1", "issue-2")
        self.run_calls = 0

    def issues(self):
        return self._issues

    def run(self, project):
        self.run_calls += 1
        return self._issues


@pytest.mark.parametrize("index", range(20))
def test_context_manager(index):
    manager = ContextManager(AssistantContext(active_level_id="L1"))
    manager.set_selection((f"E{index}",))
    assert manager.get().selected_element_ids == (f"E{index}",)
    assert manager.snapshot()["active_level_id"] == "L1"
    manager.clear_selection()
    assert manager.get().selected_element_ids == ()


@pytest.mark.parametrize("index", range(20))
def test_conversation_memory(index):
    memory = ConversationMemory(max_entries=2)
    memory.add("user", f"Pregunta {index}")
    memory.add("assistant", "Respuesta")
    memory.add("system", "Contexto")
    assert len(memory) == 2
    assert memory.recent(1)[0].content == "Contexto"
    memory.clear()
    assert len(memory) == 0


@pytest.mark.parametrize("index", range(20))
def test_prompt_parser(index):
    parser = PromptParser()
    assert parser.parse("¿Qué elemento está seleccionado?").intent_type is IntentType.QUERY_SELECTION
    assert parser.parse("¿Cuántas columnas existen?").intent_type is IntentType.QUERY_COUNTS
    assert parser.parse("¿Qué problemas tiene el proyecto?").intent_type is IntentType.QUERY_ISSUES
    intent = parser.parse("Aumenta ancho a 0,90")
    assert intent.intent_type is IntentType.MODIFY_PROPERTY
    assert intent.entities["value"] == pytest.approx(0.90)


@pytest.mark.parametrize("index", range(20))
def test_planner(index):
    parser = PromptParser()
    planner = Planner()
    plan = planner.create_plan(parser.parse("Revisa el proyecto"))
    assert not plan.is_empty
    assert plan.steps[0].action.action_type == "run_rules"
    unknown = planner.create_plan(parser.parse("xyz"))
    assert unknown.is_empty


@pytest.mark.parametrize("index", range(20))
def test_dispatcher(index):
    project = {
        "elements": [
            {"element_id": "C1", "kind": "column"},
            {"element_id": "D1", "kind": "door"},
            {"element_id": "C2", "kind": "column"},
        ]
    }
    manager = ContextManager(
        AssistantContext(
            project=project,
            selected_element_ids=(f"E{index}",),
        )
    )
    dispatcher = ActionDispatcher(manager)

    count_result = dispatcher.dispatch(
        AssistantAction("a1", "query_counts", {"entity": "columnas"})
    )
    assert count_result.status is ActionStatus.COMPLETED
    assert count_result.value == 2

    selection_result = dispatcher.dispatch(
        AssistantAction("a2", "query_selection")
    )
    assert selection_result.value == (f"E{index}",)


@pytest.mark.parametrize("index", range(20))
def test_assistant_integration(index):
    project = {"elements": [{"element_id": "D1", "kind": "door"}]}
    rule_engine = FakeRuleEngine()
    assistant = AIDesignAssistant(
        context_manager=ContextManager(
            AssistantContext(
                project=project,
                selected_element_ids=(f"E{index}",),
            )
        ),
        services={"rule_engine": rule_engine},
    )

    response = assistant.ask("¿Qué problemas tiene el proyecto?")
    assert response.kind.value == "action_result"
    assert "2" in response.text
    assert len(assistant.history()) == 2
    assert assistant.context().selected_element_ids == (f"E{index}",)
    assert len(assistant.suggestions()) >= 3
