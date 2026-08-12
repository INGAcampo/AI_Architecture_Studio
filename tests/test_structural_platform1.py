import json
from pathlib import Path
import pytest
from aias_structural_platform1 import StructuralModel, AnalysisModel, DesignEngine
ROOT=Path(__file__).resolve().parents[1]
def test_structural_layers_prepare_without_merging_analysis_and_design():
    result=DesignEngine().prepare(StructuralModel("bldg-1",("beam-1","column-1")),AnalysisModel("bldg-1",("gravity","seismic")))
    assert result["prepared"] is True and result["normative_status"] == "external_authority_pending"
def test_structural_identity_mismatch_fails_closed():
    with pytest.raises(ValueError, match="model_identity_mismatch"): DesignEngine().prepare(StructuralModel("a"),AnalysisModel("b"))
def test_structural_spec_preserves_professional_gates():
    spec=json.loads((ROOT/"engineering/aias/structural_platform1/STRUCTURAL_PLATFORM_1_SPEC.json").read_text(encoding="utf-8"))
    assert "Standards Engine" in spec["layers"] and "licensed Venezuelan standards" in spec["non_claims"]
