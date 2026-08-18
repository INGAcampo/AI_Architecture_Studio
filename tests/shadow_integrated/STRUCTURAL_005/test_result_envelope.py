from structural_platform_results.envelope import ScalarResult,envelope_results
from structural_platform_results.combination import CombinationFactor,combine_scalar_results


def test_envelope_finds_min_max_and_absolute_governing():
    env=envelope_results(
        (
            ScalarResult("A",-20.0),
            ScalarResult("B",15.0),
            ScalarResult("C",5.0),
        )
    )
    assert env.minimum.source_case=="A"
    assert env.maximum.source_case=="B"
    assert env.absolute_governing.source_case=="A"


def test_scalar_combination_is_deterministic():
    result=combine_scalar_results(
        {"D":100.0,"L":50.0},
        (
            CombinationFactor("D",1.2),
            CombinationFactor("L",1.6),
        ),
        "1.2D+1.6L",
    )
    assert result.source_case=="1.2D+1.6L"
    assert result.value==200.0


def test_missing_combination_case_fails_closed():
    failed=False
    try:
        combine_scalar_results(
            {"D":100.0},
            (CombinationFactor("L",1.6),),
            "BAD",
        )
    except KeyError:
        failed=True
    assert failed is True
