import pytest

from aias_capability_factory import CompleteVerticalGate


def complete(**overrides):
    evidence = {
        "specification":"SPEC-001","architecture":"ARCH-001","implementation":"src/example.py",
        "consumer":"workspace.command:EXAMPLE","tests":"tests/test_example.py","documentation":"docs/EXAMPLE.md",
        "installer":"AIAS_EXAMPLE_INSTALLER","traceability":"engineering/example/TRACEABILITY.json","reference_case":"CASE-EXAMPLE-001",
    }
    evidence.update(overrides)
    return evidence


def test_base_vertical_passes_only_with_real_consumer_and_reference_case():
    gate = CompleteVerticalGate()
    assert gate.require(complete(), user_facing=False, regulated=False).passed
    with pytest.raises(ValueError, match="consumer_is_not_materialized"):
        gate.require(complete(consumer="PLANNED"), user_facing=False, regulated=False)
    with pytest.raises(ValueError, match="reference_case_is_not_materialized"):
        gate.require(complete(reference_case="FUTURE"), user_facing=False, regulated=False)


def test_user_facing_vertical_requires_interface_and_rendered_review():
    result = CompleteVerticalGate().evaluate(complete(), user_facing=True, regulated=False)
    assert not result.passed and result.missing == ("interface", "rendered_review")
    assert CompleteVerticalGate().require(complete(interface="workspace.panel:EXAMPLE", rendered_review="outputs/example.png"), user_facing=True, regulated=False).passed


def test_regulated_vertical_requires_normative_and_professional_boundaries():
    result = CompleteVerticalGate().evaluate(complete(), user_facing=False, regulated=True)
    assert result.missing == ("normative_boundary", "professional_review_boundary")
    evidence = complete(normative_boundary="REFERENCE_ONLY_UNTIL_LICENSED", professional_review_boundary="LICENSED_ENGINEER_REQUIRED")
    assert CompleteVerticalGate().require(evidence, user_facing=False, regulated=True).passed


def test_missing_multiple_evidence_is_reported_deterministically():
    result = CompleteVerticalGate().evaluate({"specification":"SPEC-1"}, user_facing=False, regulated=False)
    assert result.present == ("specification",)
    assert result.missing[0] == "architecture" and "reference_case" in result.missing
