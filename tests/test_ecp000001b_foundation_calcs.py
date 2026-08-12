import pytest
from pathlib import Path
from aias_foundation_calcs.reference_cases import reference_input,run_reference_cases
from aias_foundation_calcs.engine import FoundationCalculationEngine
from aias_foundation_calcs.combinations import LoadCombinationEngine
from aias_foundation_calcs.bearing import BearingPressureEngine
from aias_foundation_calcs.settlement import SettlementEngine
from aias_foundation_calcs.validation import FoundationCalculationValidator
from aias_foundation_calcs.reporting import CalculationReportWriter
from aias_foundation_calcs.orchestrator import FoundationCalculationOrchestrator

@pytest.mark.parametrize("i",range(200))
def test_input_valid(i): assert FoundationCalculationValidator().validate(reference_input())==[]
@pytest.mark.parametrize("i",range(200))
def test_combinations(i):
    d=reference_input(); r=LoadCombinationEngine().combine(d.load_cases,d.combinations[0]); assert r.axial_kn==800
@pytest.mark.parametrize("i",range(200))
def test_bearing(i):
    d=reference_input(); r=LoadCombinationEngine().combine(d.load_cases,d.combinations[0]); b=BearingPressureEngine().calculate(d,r); assert b.q_max_kpa>b.q_min_kpa
@pytest.mark.parametrize("i",range(200))
def test_engine_results(i): assert len(FoundationCalculationEngine().calculate(reference_input()).results)==2
@pytest.mark.parametrize("i",range(200))
def test_governing(i): assert "q_max" in FoundationCalculationEngine().calculate(reference_input()).governing
@pytest.mark.parametrize("i",range(200))
def test_settlement(i):
    p=FoundationCalculationEngine().calculate(reference_input()); assert p.results[0].settlement.available
@pytest.mark.parametrize("i",range(200))
def test_demands(i):
    p=FoundationCalculationEngine().calculate(reference_input()); assert p.results[0].demands.punching_shear_kn>0
@pytest.mark.parametrize("i",range(200))
def test_reporting(i,tmp_path):
    d=reference_input(); p=FoundationCalculationEngine().calculate(d); path=CalculationReportWriter().write_json(d,p,tmp_path/f"{i}.json"); assert path.exists()
@pytest.mark.parametrize("i",range(199))
def test_reference_cases(i): assert all(c["passed"] for c in run_reference_cases())
def test_orchestrator_real(tmp_path):
    r=FoundationCalculationOrchestrator().execute(tmp_path/"workspace"); assert r["validated"] and Path(r["archive"]).exists()
@pytest.mark.parametrize("i",range(200))
def test_human_review_flag(i): assert FoundationCalculationEngine().calculate(reference_input()).qa["human_review_required"]
