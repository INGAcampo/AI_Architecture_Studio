from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class MultiObjectiveSolution:
    solution_id: str
    objectives: dict[str, float]
    metadata: dict

@dataclass(frozen=True, slots=True)
class Recommendation:
    solution_id: str
    rank: int
    explanation: str

class ParetoRecommendationEngine:
    def dominates(self, left, right, *, minimize):
        keys = tuple(minimize)
        no_worse = all(left.objectives[k] <= right.objectives[k] for k in keys)
        strictly_better = any(left.objectives[k] < right.objectives[k] for k in keys)
        return no_worse and strictly_better

    def pareto_front(self, solutions, *, minimize):
        solutions = tuple(solutions)
        front = []
        for candidate in solutions:
            if not any(
                other.solution_id != candidate.solution_id
                and self.dominates(other, candidate, minimize=minimize)
                for other in solutions
            ):
                front.append(candidate)
        return tuple(sorted(front, key=lambda solution: solution.solution_id))

    def recommend(self, solutions, *, minimize, weights):
        front = self.pareto_front(solutions, minimize=minimize)
        scored = []
        for solution in front:
            score = sum(solution.objectives[key] * weights.get(key, 1.0) for key in minimize)
            scored.append((score, solution))
        scored.sort(key=lambda item: item[0])
        return tuple(
            Recommendation(
                solution_id=solution.solution_id,
                rank=index + 1,
                explanation=f"Solución Pareto con puntuación ponderada {score:.3f}",
            )
            for index, (score, solution) in enumerate(scored)
        )
