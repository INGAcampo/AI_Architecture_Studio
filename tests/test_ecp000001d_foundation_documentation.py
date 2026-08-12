from pathlib import Path

import pytest

from aias_foundation_calcs.engine import FoundationCalculationEngine
from aias_foundation_calcs.reference_cases import reference_input as calculation_input
from aias_foundation_code_checks.engine import FoundationCodeCheckEngine
from aias_foundation_code_checks.reference_pack import generic_reference_pack, reference_input as check_input
from aias_foundation_documentation.detailing import ReinforcementDetailer
from aias_foundation_documentation.engine import FoundationDocumentationEngine
from aias_foundation_documentation.orchestrator import FoundationDocumentationOrchestrator
from aias_foundation_documentation.quantities import QuantityEngine
from aias_foundation_documentation.reference_cases import reference_package, run_reference_cases
from aias_foundation_documentation.reporting import DocumentationWriter
from aias_foundation_objects.reference_cases import reference_objects


@pytest.fixture
def inputs():
    foundation = reference_objects()["isolated"]
    calculation = FoundationCalculationEngine().calculate(calculation_input())
    checks = FoundationCodeCheckEngine().check(check_input(), generic_reference_pack())
    return foundation, calculation, checks


def test_detailer_produces_two_orthogonal_marks(inputs):
    foundation, _, checks = inputs
    bars = ReinforcementDetailer().detail(foundation, checks.reinforcement)
    assert [bar.direction for bar in bars] == ["X", "Y"]
    assert all(75 <= bar.spacing_mm <= 300 for bar in bars)


def test_quantities_are_positive(inputs):
    foundation, _, checks = inputs
    bars = ReinforcementDetailer().detail(foundation, checks.reinforcement)
    quantities = QuantityEngine().calculate(foundation, bars)
    assert quantities.concrete_m3 == foundation.geometry.volume_m3
    assert quantities.reinforcement_kg > 0


def test_engine_consumes_a_b_and_c(inputs, tmp_path):
    foundation, calculation, checks = inputs
    package = FoundationDocumentationEngine().generate(foundation, calculation, checks, tmp_path)
    assert package.traceability == {
        "object_source": "ECP-000001A",
        "calculation_source": "ECP-000001B",
        "check_source": "ECP-000001C",
        "document_source": "ECP-000001D",
    }
    assert len(package.drawing_manifest) == 2


def test_svg_drawings_exist(inputs, tmp_path):
    package = FoundationDocumentationEngine().generate(*inputs, tmp_path)
    for item in package.drawing_manifest:
        path = Path(item["path"])
        assert path.exists()
        assert path.read_text(encoding="utf-8").startswith("<svg")


def test_document_writer_creates_json_csv_and_markdown(tmp_path):
    package = reference_package(tmp_path / "generation")
    files = DocumentationWriter().write(package, tmp_path / "workspace")
    assert {Path(path).suffix for path in files.values()} == {".json", ".csv", ".md"}
    assert all(Path(path).exists() for path in files.values())


def test_reference_cases_pass(tmp_path):
    cases = run_reference_cases(tmp_path)
    assert len(cases) == 8
    assert all(case["passed"] for case in cases)


def test_reference_only_status_is_preserved(inputs, tmp_path):
    package = FoundationDocumentationEngine().generate(*inputs, tmp_path)
    assert package.qa["legal_status"] == "REFERENCE_ONLY"
    assert package.qa["verified_official_required_for_construction"]


def test_human_review_is_mandatory(inputs, tmp_path):
    package = FoundationDocumentationEngine().generate(*inputs, tmp_path)
    assert package.qa["human_review_required"] is True


def test_empty_calculations_are_rejected(inputs, tmp_path):
    foundation, calculation, checks = inputs
    calculation.results.clear()
    with pytest.raises(ValueError, match="calculation_package_has_no_results"):
        FoundationDocumentationEngine().generate(foundation, calculation, checks, tmp_path)


def test_orchestrator_produces_release(tmp_path):
    result = FoundationDocumentationOrchestrator().execute(tmp_path / "workspace")
    assert result["validated"]
    assert result["reference_cases"] == 8
    assert result["drawings"] == 2
    assert Path(result["archive"]).exists()
    assert len(result["sha256"]) == 64
