import pytest

from ai_kernel import (
    AIGenerativeKernel,
    AsyncExecutionScheduler,
    CandidateStatus,
    ConstraintAdapter,
    DesignCandidate,
    EvaluationContext,
    EvaluationPipeline,
    KernelTransaction,
    MetricsEngine,
    Objective,
    ObjectiveDirection,
    OptimizerPlugin,
    OptimizerPluginRegistry,
    PopulationManager,
)


@pytest.mark.parametrize("index", range(20))
def test_candidate_and_context(index):
    context = EvaluationContext(f"P{index}", "architecture")
    candidate = DesignCandidate({"area": 100 + index}, generation=index)
    assert context.project_id == f"P{index}"
    assert candidate.parameters["area"] == 100 + index
    assert candidate.with_status(CandidateStatus.SELECTED).status is CandidateStatus.SELECTED


@pytest.mark.parametrize("index", range(20))
def test_objectives(index):
    candidate = DesignCandidate({"cost": 1000 + index, "quality": 80})
    cost = Objective(
        "cost",
        lambda c: c.parameters["cost"],
        direction=ObjectiveDirection.MINIMIZE,
        weight=2.0,
    )
    quality = Objective(
        "quality",
        lambda c: c.parameters["quality"],
        direction=ObjectiveDirection.MAXIMIZE,
    )
    assert cost.evaluate(candidate).normalized_score == -(1000 + index) * 2
    assert quality.evaluate(candidate).normalized_score == 80


@pytest.mark.parametrize("index", range(20))
def test_constraints_and_evaluation(index):
    candidate = DesignCandidate({"width": 0.9, "cost": 100 + index})
    constraints = ConstraintAdapter()
    constraints.register("min-width", lambda c: c.parameters["width"] >= 0.8)
    objectives = (
        Objective("cost", lambda c: c.parameters["cost"]),
    )
    report = EvaluationPipeline(objectives, constraints).evaluate(candidate)
    assert report.feasible
    assert report.total_score == -(100 + index)


@pytest.mark.parametrize("index", range(20))
def test_population_and_metrics(index):
    manager = PopulationManager()
    reports = []
    constraints = ConstraintAdapter()
    objective = Objective("value", lambda c: c.parameters["value"])
    pipeline = EvaluationPipeline((objective,), constraints)

    for value in (1, 2, 3):
        candidate = DesignCandidate({"value": value + index})
        manager.add(candidate)
        reports.append(pipeline.evaluate(candidate))

    snapshot = manager.snapshot()
    metrics = MetricsEngine().summarize(reports)
    assert snapshot.size == 3
    assert metrics.evaluated_count == 3
    assert metrics.feasible_count == 3


@pytest.mark.parametrize("index", range(20))
def test_scheduler_and_transaction(index):
    scheduler = AsyncExecutionScheduler(max_workers=2)
    results = scheduler.map(lambda value: value * 2, (1, 2, 3))
    assert tuple(result.value for result in results) == (2, 4, 6)

    manager = PopulationManager()
    transaction = KernelTransaction(manager)

    outcome = transaction.commit(
        lambda: manager.add(DesignCandidate({"x": index}))
    )
    assert outcome.committed
    assert manager.snapshot().size == 1


@pytest.mark.parametrize("index", range(20))
def test_kernel_and_plugins(index):
    class KeepBestPlugin(OptimizerPlugin):
        plugin_id = "keep-best"

        def optimize(self, kernel, population):
            return max(
                population.all(),
                key=lambda c: c.parameters["score"],
            )

    constraints = ConstraintAdapter()
    pipeline = EvaluationPipeline(
        (Objective("score", lambda c: c.parameters["score"], direction=ObjectiveDirection.MAXIMIZE),),
        constraints,
    )
    kernel = AIGenerativeKernel(pipeline)
    kernel.add_candidate(DesignCandidate({"score": index}))
    kernel.add_candidate(DesignCandidate({"score": index + 10}))
    kernel.plugins.register(KeepBestPlugin())

    reports = kernel.evaluate_all()
    assert len(reports) == 2
    assert kernel.metrics_snapshot().evaluated_count == 2
    assert kernel.run_plugin("keep-best").parameters["score"] == index + 10
