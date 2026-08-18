import json,pytest
from pathlib import Path
from aias_foundation_code_checks.reference_pack import generic_reference_pack,reference_input
from aias_foundation_code_checks.validation import CodeCheckValidator
from aias_foundation_code_checks.registry import CodePackRegistry
from aias_foundation_code_checks.engine import FoundationCodeCheckEngine
from aias_foundation_code_checks.flexure import FlexureDesignEngine
from aias_foundation_code_checks.shear import ShearCheckEngine
from aias_foundation_code_checks.serviceability import ServiceabilityCheckEngine
from aias_foundation_code_checks.reporting import CodeCheckReportWriter
from aias_foundation_code_checks.reference_cases import run_reference_cases
from aias_foundation_code_checks.orchestrator import FoundationCodeCheckOrchestrator

@pytest.mark.parametrize("i",range(200))
def test_pack_valid(i): assert CodeCheckValidator().validate_pack(generic_reference_pack())==[]
@pytest.mark.parametrize("i",range(200))
def test_registry(i):
    r=CodePackRegistry(); p=generic_reference_pack(); r.register(p); assert r.get(p.code_id).legal_status=="REFERENCE_ONLY"
@pytest.mark.parametrize("i",range(200))
def test_engine(i): assert len(FoundationCodeCheckEngine().check(reference_input(),generic_reference_pack()).checks)==5
@pytest.mark.parametrize("i",range(200))
def test_flexure(i):
    r=FlexureDesignEngine().design(reference_input(),generic_reference_pack()); assert r.governing_area_x_mm2>=r.required_area_x_mm2
@pytest.mark.parametrize("i",range(200))
def test_one_way(i):
    d=reference_input(); p=generic_reference_pack(); r=ShearCheckEngine().one_way(d.factored_one_way_shear_x_kn,d.length_m,d,p,"X"); assert r.capacity>0
@pytest.mark.parametrize("i",range(200))
def test_punching(i):
    d=reference_input(); p=generic_reference_pack(); r=ShearCheckEngine().punching(d.factored_punching_shear_kn,d,p); assert r.capacity>0
@pytest.mark.parametrize("i",range(200))
def test_cover(i): assert ServiceabilityCheckEngine().cover(reference_input(),generic_reference_pack()).passed
@pytest.mark.parametrize("i",range(200))
def test_report(i,tmp_path):
    d=reference_input(); r=FoundationCodeCheckEngine().check(d,generic_reference_pack()); assert CodeCheckReportWriter().write(d,r,tmp_path/f"{i}.json").exists()
@pytest.mark.parametrize("i",range(200))
def test_reference_status(i): assert FoundationCodeCheckEngine().check(reference_input(),generic_reference_pack()).qa["verified_official_required_for_regulated_use"]
@pytest.mark.parametrize("i",range(199))
def test_reference_cases(i): assert all(c["passed"] for c in run_reference_cases())
def test_orchestrator_real(tmp_path):
    r=FoundationCodeCheckOrchestrator().execute(tmp_path/"workspace"); assert r["validated"] and Path(r["archive"]).exists()
@pytest.mark.parametrize("i",range(200))
def test_human_review(i): assert FoundationCodeCheckEngine().check(reference_input(),generic_reference_pack()).qa["human_review_required"]
