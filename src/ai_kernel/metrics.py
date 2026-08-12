from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class MetricsSnapshot:
    evaluated_count: int
    feasible_count: int
    rejected_count: int
    average_score: float

class MetricsEngine:
    def summarize(self, reports):
        reports = tuple(reports)
        if not reports:
            return MetricsSnapshot(0, 0, 0, 0.0)
        feasible = sum(report.feasible for report in reports)
        rejected = len(reports) - feasible
        average = sum(report.total_score for report in reports) / len(reports)
        return MetricsSnapshot(len(reports), feasible, rejected, average)
