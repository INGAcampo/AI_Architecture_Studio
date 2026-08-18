from dataclasses import dataclass
from .candidate import CandidateStatus

@dataclass(frozen=True, slots=True)
class EvaluationReport:
    candidate_id: str
    feasible: bool
    objective_results: tuple
    constraint_checks: tuple
    total_score: float

class EvaluationPipeline:
    def __init__(self, objectives, constraint_adapter):
        self.objectives = tuple(objectives)
        self.constraint_adapter = constraint_adapter

    def evaluate(self, candidate):
        checks = self.constraint_adapter.check(candidate)
        feasible = all(check.passed for check in checks)
        objective_results = tuple(
            objective.evaluate(candidate) for objective in self.objectives
        )
        total_score = sum(result.normalized_score for result in objective_results)
        return EvaluationReport(
            candidate_id=candidate.candidate_id,
            feasible=feasible,
            objective_results=objective_results,
            constraint_checks=checks,
            total_score=total_score,
        )
