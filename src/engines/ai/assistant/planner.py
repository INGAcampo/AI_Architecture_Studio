from __future__ import annotations
from dataclasses import dataclass

from .action import AssistantAction
from .intent import AssistantIntent, IntentType


@dataclass(frozen=True, slots=True)
class PlanStep:
    step_number: int
    action: AssistantAction


@dataclass(frozen=True, slots=True)
class AssistantPlan:
    intent: AssistantIntent
    steps: tuple[PlanStep, ...]

    @property
    def is_empty(self) -> bool:
        return not self.steps


class Planner:
    def create_plan(self, intent: AssistantIntent) -> AssistantPlan:
        mapping = {
            IntentType.QUERY_SELECTION: "query_selection",
            IntentType.QUERY_COUNTS: "query_counts",
            IntentType.QUERY_ISSUES: "query_issues",
            IntentType.QUERY_CONTEXT: "query_context",
            IntentType.MODIFY_PROPERTY: "modify_property",
            IntentType.RUN_RULES: "run_rules",
        }
        action_type = mapping.get(intent.intent_type)
        if action_type is None:
            return AssistantPlan(intent, ())

        action = AssistantAction(
            action_id=f"{intent.intent_type.value}.1",
            action_type=action_type,
            payload=dict(intent.entities),
        )
        return AssistantPlan(intent, (PlanStep(1, action),))
