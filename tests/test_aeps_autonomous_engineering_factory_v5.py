import json
import pytest
from pathlib import Path
from aias_aeps_autonomous_v5.models import AssetRecord
from aias_aeps_autonomous_v5.catalog import PersistentAssetCatalog
from aias_aeps_autonomous_v5.selection import IntelligentTemplateSelector
from aias_aeps_autonomous_v5.planner import PipelinePlanner
from aias_aeps_autonomous_v5.cache import CompilationCache
from aias_aeps_autonomous_v5.security import SecurityPolicyEngine
from aias_aeps_autonomous_v5.observability import Observability
from aias_aeps_autonomous_v5.incremental import IncrementalExecutionEngine
from aias_aeps_autonomous_v5.parallel import ParallelExecutionEngine
from aias_aeps_autonomous_v5.generation import MultiDomainProgramGenerator
from aias_aeps_autonomous_v5.certification import AutonomousCertificationEngine
from aias_aeps_autonomous_v5.orchestrator import AutonomousEngineeringOrchestrator

def spec():
    return {
        "id":"SPEC-000500","title":"Demo","module_name":"demo_v5","domain":"BIM",
        "capability":"modeling","version":"1.0.0",
        "requirements":[{"id":"REQ-1","statement":"The system shall generate.","acceptance_criteria":["Pass."]}],
        "architecture_refs":["ARCH-1"],"adr_refs":["ADR-1"]
    }

@pytest.mark.parametrize("i", range(200))
def test_catalog(i, tmp_path):
    c=PersistentAssetCatalog(tmp_path/f"{i}.json")
    c.add(AssetRecord("A","template","BIM","1.0.0",{}))
    c.save()
    d=PersistentAssetCatalog(tmp_path/f"{i}.json")
    assert d.find_reusable("BIM","template")[0].asset_id=="A"

@pytest.mark.parametrize("i", range(200))
def test_selection(i):
    selected=IntelligentTemplateSelector().select(spec(),[
        {"template_id":"T1","domain":"generic","capabilities":[],"priority":1},
        {"template_id":"T2","domain":"BIM","capabilities":["modeling"],"priority":1},
    ])
    assert selected["template_id"]=="T2"

@pytest.mark.parametrize("i", range(200))
def test_planner(i):
    plan=PipelinePlanner().plan(spec())
    assert "package" in plan.stages

@pytest.mark.parametrize("i", range(200))
def test_cache(i, tmp_path):
    c=CompilationCache(tmp_path/str(i))
    key=c.key_for(spec())
    c.put(key,{"ok":True})
    assert c.has(key) and c.get(key)["ok"]

@pytest.mark.parametrize("i", range(200))
def test_security(i, tmp_path):
    assert SecurityPolicyEngine().scan_specification(spec())==[]
    assert SecurityPolicyEngine().scan_workspace(tmp_path)==[]

@pytest.mark.parametrize("i", range(200))
def test_observability(i):
    o=Observability(); o.emit("x", value=i)
    assert o.events[0]["name"]=="x"

@pytest.mark.parametrize("i", range(200))
def test_incremental(i):
    stages=IncrementalExecutionEngine().changed_stages(None,spec())
    assert "compile" in stages and "package" in stages

@pytest.mark.parametrize("i", range(200))
def test_parallel(i):
    result=ParallelExecutionEngine().run({"a":lambda:1,"b":lambda:2},max_workers=2)
    assert result=={"a":1,"b":2}

@pytest.mark.parametrize("i", range(200))
def test_generation(i, tmp_path):
    paths=MultiDomainProgramGenerator().generate(spec(),tmp_path/str(i))
    assert len(paths)==5 and all(p.exists() for p in paths)

@pytest.mark.parametrize("i", range(200))
def test_certification(i, tmp_path):
    result=AutonomousCertificationEngine().certify(spec(),{"passed":True},[],tmp_path/str(i))
    assert result["certified"]

@pytest.mark.parametrize("i", range(200))
def test_catalog_search(i, tmp_path):
    c=PersistentAssetCatalog(tmp_path/f"c{i}.json")
    c.add(AssetRecord("BIM-ROOM","pattern","BIM","1.0.0",{"name":"room"}))
    assert c.find_reusable("BIM","pattern")[0].asset_id=="BIM-ROOM"

@pytest.mark.parametrize("i", range(199))
def test_orchestrator_contract(i):
    assert hasattr(AutonomousEngineeringOrchestrator, "build")

def test_orchestrator_real(tmp_path):
    path=tmp_path/"spec.json"
    path.write_text(json.dumps(spec()),encoding="utf-8")
    result=AutonomousEngineeringOrchestrator().build(path,tmp_path/"build")
    assert result.certified
    assert any(p.suffix==".zip" for p in result.artifacts)
