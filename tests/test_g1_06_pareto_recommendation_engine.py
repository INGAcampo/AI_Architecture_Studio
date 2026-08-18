import pytest
from ai_kernel.pareto_recommendation import *

@pytest.mark.parametrize("i", range(120))
def test_pareto(i):
    solutions = (
        MultiObjectiveSolution("A", {"cost": 100, "energy": 80}, {}),
        MultiObjectiveSolution("B", {"cost": 90, "energy": 90}, {}),
        MultiObjectiveSolution("C", {"cost": 120, "energy": 100}, {}),
    )
    engine = ParetoRecommendationEngine()
    front = engine.pareto_front(solutions, minimize=("cost", "energy"))
    assert tuple(solution.solution_id for solution in front) == ("A", "B")
    recommendations = engine.recommend(
        solutions,
        minimize=("cost", "energy"),
        weights={"cost": 1.0, "energy": 1.0},
    )
    assert len(recommendations) == 2
    assert recommendations[0].rank == 1
