from shadow_test_factory.contracts import GoldenCase, TestPolicy
from shadow_test_factory.runner import GoldenCaseRunner


def test_runner_passes_deterministic_golden_cases():
    cases = [
        GoldenCase("sum", "sum is deterministic", lambda: 1 + 2, 3),
        GoldenCase("len", "length is deterministic", lambda: len("aias"), 4),
    ]

    record = GoldenCaseRunner().run("suite-1", cases)

    assert record.all_passed is True
    assert record.passed_count == 2
    assert record.failed_count == 0


def test_runner_records_exception_as_failure():
    def boom():
        raise RuntimeError("expected")

    cases = [
        GoldenCase("boom", "records exceptions", boom, "never"),
    ]

    record = GoldenCaseRunner().run("suite-2", cases)

    assert record.all_passed is False
    assert record.failed_count == 1
    assert "RuntimeError" in record.results[0].error


def test_fail_fast_stops_after_first_failure():
    calls = []

    cases = [
        GoldenCase("bad", "fails", lambda: 1, 2),
        GoldenCase("later", "must not execute", lambda: calls.append(1), None),
    ]

    runner = GoldenCaseRunner(TestPolicy(fail_fast=True))
    record = runner.run("suite-3", cases)

    assert len(record.results) == 1
    assert calls == []
