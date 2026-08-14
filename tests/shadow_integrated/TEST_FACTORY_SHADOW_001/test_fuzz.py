from shadow_test_factory.fuzz import run_numeric_invariant_fuzz


def test_fuzz_is_reproducible_for_same_seed():
    invariant = lambda value: -10.0 <= value <= 10.0

    first = run_numeric_invariant_fuzz(
        invariant,
        seed=123,
        iterations=100,
        low=-20.0,
        high=20.0,
    )
    second = run_numeric_invariant_fuzz(
        invariant,
        seed=123,
        iterations=100,
        low=-20.0,
        high=20.0,
    )

    assert first == second


def test_fuzz_reports_zero_failures_for_true_invariant():
    result = run_numeric_invariant_fuzz(
        lambda value: value == value,
        seed=5,
        iterations=200,
    )

    assert result.failures == 0
