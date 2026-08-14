from shadow_test_factory.benchmark import benchmark


def test_benchmark_returns_positive_metrics():
    result = benchmark(
        "increment",
        lambda: 1 + 1,
        iterations=1000,
    )

    assert result.iterations == 1000
    assert result.elapsed_seconds >= 0
    assert result.operations_per_second > 0
