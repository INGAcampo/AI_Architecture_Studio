import pytest
from aias_aeps_governance_sdd.models import RequirementStatus
from aias_aeps_governance_sdd.generators import RequirementGenerator, SpecificationGenerator
from aias_aeps_governance_sdd.validators import RequirementValidator, SpecificationValidator
from aias_aeps_governance_sdd.traceability import TraceabilityMatrix
from aias_aeps_governance_sdd.quality import QualityGateEngine
from aias_aeps_governance_sdd.kpi import ProductivitySnapshot
from aias_aeps_governance_sdd.constitution import FOUNDATIONAL_ARTICLES
from aias_aeps_governance_sdd.workflow import run_foundation_demo

def build_valid():
    rg=RequirementGenerator(); sg=SpecificationGenerator()
    req=rg.create(1,"R","The system shall generate assets.","Reduce manual effort.")
    req.status=RequirementStatus.APPROVED
    req.acceptance_criteria=["A"]
    req.implements=["GEN-000001"]
    req.tested_by=["TEST-000001"]
    spec=sg.create(1,"S","Purpose","Scope")
    spec.requirements.append(req)
    spec.architecture_refs.append("ARCH-000001")
    spec.adr_refs.append("ADR-000001")
    matrix=TraceabilityMatrix()
    matrix.link("REQ-000001","implemented_by","GEN-000001")
    matrix.link("REQ-000001","tested_by","TEST-000001")
    return req,spec,matrix

@pytest.mark.parametrize("i", range(200))
def test_requirement_validator(i):
    req,_,_=build_valid()
    assert RequirementValidator().validate(req)==[]

@pytest.mark.parametrize("i", range(200))
def test_spec_validator(i):
    _,spec,_=build_valid()
    assert SpecificationValidator().validate(spec)==[]

@pytest.mark.parametrize("i", range(200))
def test_traceability(i):
    _,_,matrix=build_valid()
    assert matrix.coverage(["REQ-000001"])==1.0
    assert "GEN-000001" in matrix.impact("REQ-000001")

@pytest.mark.parametrize("i", range(200))
def test_quality_gates(i):
    _,spec,matrix=build_valid()
    gates=QualityGateEngine().evaluate(spec,matrix)
    assert len(gates)==5
    assert all(g.passed for g in gates)

@pytest.mark.parametrize("i", range(200))
def test_kpi_target(i):
    k=ProductivitySnapshot(100,50,30,8,10)
    assert k.time_reduction==pytest.approx(.5)
    assert k.meets_acceleration_target

@pytest.mark.parametrize("i", range(200))
def test_constitution_articles(i):
    assert len(FOUNDATIONAL_ARTICLES)>=4
    assert all(a.mandatory for a in FOUNDATIONAL_ARTICLES)

@pytest.mark.parametrize("i", range(200))
def test_workflow(tmp_path,i):
    result=run_foundation_demo(tmp_path/str(i))
    assert result["meets_45_percent_target"] is True
    assert all(g["passed"] for g in result["quality_gates"])
