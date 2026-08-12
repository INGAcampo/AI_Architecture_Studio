"""Controlled engineering-object lifecycle with explicit quality-state side effects."""
from __future__ import annotations
from .models import EngineeringState

class StateMachine:
    """Reject illegal lifecycle jumps and increment revision on every accepted change."""
    ALLOWED = {
        "DRAFT":{"VALIDATED","RETIRED"},
        "VALIDATED":{"CALCULATED","RETIRED"},
        "CALCULATED":{"QA_PASSED","QA_FAILED","RETIRED"},
        "QA_FAILED":{"CALCULATED","RETIRED"},
        "QA_PASSED":{"DOCUMENTED","RETIRED"},
        "DOCUMENTED":{"RELEASED","RETIRED"},
        "RELEASED":{"RETIRED"},
        "RETIRED":set(),
    }

    def transition(self, state: EngineeringState, target: str) -> None:
        """Apply a legal lifecycle transition and update revision and QA substates."""
        if target not in self.ALLOWED.get(state.lifecycle,set()):
            raise ValueError(f"invalid_transition:{state.lifecycle}->{target}")
        state.lifecycle = target
        state.revision += 1
        if target == "CALCULATED":
            state.calculation_status = "COMPLETE"
        elif target == "QA_PASSED":
            state.qa_status = "PASS"
        elif target == "QA_FAILED":
            state.qa_status = "FAIL"
        elif target == "DOCUMENTED":
            state.documentation_status = "COMPLETE"
