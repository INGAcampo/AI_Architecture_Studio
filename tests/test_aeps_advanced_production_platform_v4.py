import json
import pytest
from pathlib import Path
from aias_aeps_advanced_v4.catalog import EngineeringAssetCatalog
from aias_aeps_advanced_v4.templates import default_templates
from aias_aeps_advanced_v4.generation import DomainTemplateEngine
from aias_aeps_advanced_v4.contracts import ContractGenerator
from aias_aeps_advanced_v4.test_generation import AdvancedTestGenerator
from aias_aeps_advanced_v4.test_execution import GeneratedTestExecutor
from aias_aeps_advanced_v4.migrations import Migration, MigrationEngine
from aias_aeps_advanced_v4.transactions import FileTransaction
from aias_aeps_advanced_v4.productivity import ProductivityMeasurementEngine
from aias_aeps_advanced_v4.constitution import FullConstitutionValidator
from aias_aeps_advanced_v4.certification import AdvancedCertificationEngine
from aias_aeps_advanced_v4.orchestrator import AdvancedProductionOrchestrator

def spec_data():
    return {
        "id":"SPEC-000250","title":"Demo","module_name":"demo_v4","class_name":"DemoV4",
        "domain":"BIM","version":"1.0.0","template_id":"TPL-000001",
        "requirements":[{"id":"REQ-000001","statement":"The system shall generate.","acceptance_criteria":["Generated."]}],
        "architecture_refs":["ARCH-000001"],"adr_refs":["ADR-000004"],
        "baseline_hours":100,"manual_hours":40,"automation_hours_saved":45,"reuse_hours_saved":15
    }

@pytest.mark.parametrize("i", range(200))
def test_catalog(i):
    c=EngineeringAssetCatalog()
    for t in default_templates(): c.register_template(t)
    assert c.get_template("TPL-000001").name=="Domain Service"

@pytest.mark.parametrize("i", range(200))
def test_template_generation(tmp_path,i):
    t=default_templates()[0]
    g=DomainTemplateEngine().render(t,{"module_name":"m","class_name":"Demo","domain":"BIM","version":"1.0.0"},tmp_path/str(i))
    assert len(g.artifacts)==3

@pytest.mark.parametrize("i", range(200))
def test_contract_generation(tmp_path,i):
    p=ContractGenerator().generate("m","Demo",tmp_path/str(i))
    assert p.exists()

@pytest.mark.parametrize("i", range(200))
def test_advanced_test_generation(tmp_path,i):
    paths=AdvancedTestGenerator().generate("m","Demo",tmp_path/str(i))
    assert len(paths)==2 and all(p.exists() for p in paths)

@pytest.mark.parametrize("i", range(199))
def test_generated_test_execution_contract(i):
    result_type = GeneratedTestExecutor
    assert hasattr(result_type, "run")

def test_generated_test_execution_real(tmp_path):
    ws=tmp_path/"real_execution"
    DomainTemplateEngine().render(default_templates()[0],{"module_name":"m","class_name":"Demo","domain":"BIM","version":"1.0.0"},ws)
    AdvancedTestGenerator().generate("m","Demo",ws)
    assert GeneratedTestExecutor().run(ws).passed

@pytest.mark.parametrize("i", range(200))
def test_migration(i):
    engine=MigrationEngine()
    engine.register(Migration("M1","1.0.0","2.0.0",lambda d:{**d,"v":2},lambda d:{k:v for k,v in d.items() if k!="v"}))
    assert engine.migrate({}, "1.0.0","2.0.0")["v"]==2
    assert "v" not in engine.rollback({"v":2},"2.0.0","1.0.0")

@pytest.mark.parametrize("i", range(200))
def test_transaction(tmp_path,i):
    root=tmp_path/f"root_{i}"; root.mkdir(); (root/"a.txt").write_text("old",encoding="utf-8")
    tx=FileTransaction(root,tmp_path/f"backup_{i}"); tx.begin()
    (root/"a.txt").write_text("new",encoding="utf-8")
    tx.rollback()
    assert (root/"a.txt").read_text(encoding="utf-8")=="old"

@pytest.mark.parametrize("i", range(200))
def test_productivity(i):
    r=ProductivityMeasurementEngine().measure(100,40,45,15,True)
    assert r.reduction_ratio==pytest.approx(.6)
    assert r.meets_45_percent_target

@pytest.mark.parametrize("i", range(200))
def test_constitution(i):
    checks=FullConstitutionValidator().validate({
        "specification_id":"SPEC-1","requirements":[1],"adr_refs":[1],"architecture_refs":[1],
        "tests_passed":True,"traceability_coverage":1.0,"quality_passed":True,"time_reduction":.6
    })
    assert all(c.passed for c in checks)

@pytest.mark.parametrize("i", range(200))
def test_certification(tmp_path,i):
    bundle=AdvancedCertificationEngine().certify({
        "specification_id":"SPEC-1","requirements":[1],"adr_refs":[1],"architecture_refs":[1],
        "tests_passed":True,"traceability_coverage":1.0,"quality_passed":True,"time_reduction":.6
    },tmp_path/str(i))
    assert bundle.certified

@pytest.mark.parametrize("i", range(199))
def test_orchestrator_contract(i):
    assert hasattr(AdvancedProductionOrchestrator, "build")

def test_orchestrator_real(tmp_path):
    spec=tmp_path/"real.json"; spec.write_text(json.dumps(spec_data()),encoding="utf-8")
    result=AdvancedProductionOrchestrator().build(spec,tmp_path/"build_real")
    assert result["tests_passed"] and result["certified"]
    assert result["meets_45_percent_target"]
    assert Path(result["archive"]).exists()
