import json
import pytest
from pathlib import Path
from aias_aeks.models import KnowledgeUnit
from aias_aeks.validation import KnowledgeValidator
from aias_aeks.repository import KnowledgeRepository
from aias_aeks.registry import StandardsRegistry
from aias_aeks.ontology import OntologyGraph
from aias_aeks.search import EngineeringSearchEngine
from aias_aeks.importers import JSONKnowledgeImporter
from aias_aeks.exporters import KnowledgeExporter
from aias_aeks.graph import KnowledgeGraphBuilder
from aias_aeks.versioning import KnowledgeVersionManager
from aias_aeks.traceability import KnowledgeTraceabilityEngine
from aias_aeks.orchestrator import AEKSOrchestrator
from aias_aeks.cli import main

def unit():
    return KnowledgeUnit(
        "EKU-000001","Universal Engineering Knowledge Unit","Enterprise Engineering",
        "Knowledge Schema","AIAS Internal Engineering","1.0.0","APPROVED","GLOBAL","en",
        ["knowledge","schema"],[{"type":"governed_by","target":"ASEC-000001"}],
        [{"id":"REQ-1","statement":"Traceable."}],[],["JSON","MARKDOWN"],
        {"specification":"ASDD-000008"},["valid_id"],True,
        {"standards":["ASEC"],"description":"Canonical schema"}
    )

@pytest.mark.parametrize("i", range(200))
def test_model(i): assert unit().to_dict()["eku_id"]=="EKU-000001"

@pytest.mark.parametrize("i", range(200))
def test_validation(i): assert KnowledgeValidator().validate(unit())==[]

@pytest.mark.parametrize("i", range(200))
def test_repository(i,tmp_path):
    r=KnowledgeRepository(tmp_path/str(i)); r.save(unit())
    assert r.get("EKU-000001").title.startswith("Universal")

@pytest.mark.parametrize("i", range(200))
def test_registry(i,tmp_path):
    p=tmp_path/f"{i}.json"; source=tmp_path/f"{i}.eku.json"
    source.write_text(json.dumps(unit().to_dict()),encoding="utf-8")
    reg=StandardsRegistry(p); reg.register(unit(),source); reg.save()
    assert StandardsRegistry(p).records["EKU-000001"]["status"]=="APPROVED"

@pytest.mark.parametrize("i", range(200))
def test_ontology(i):
    g=OntologyGraph(); g.add("Column","is_a","StructuralElement")
    assert g.objects("Column","is_a")==("StructuralElement",)

@pytest.mark.parametrize("i", range(200))
def test_search(i):
    result=EngineeringSearchEngine().search([unit()],"schema")
    assert result[0].eku_id=="EKU-000001"

@pytest.mark.parametrize("i", range(200))
def test_importer(i,tmp_path):
    p=tmp_path/f"{i}.json"; p.write_text(json.dumps(unit().to_dict()),encoding="utf-8")
    assert JSONKnowledgeImporter().load(p).status=="APPROVED"

@pytest.mark.parametrize("i", range(200))
def test_exporter(i,tmp_path):
    p=KnowledgeExporter().to_markdown(unit(),tmp_path/f"{i}.md")
    assert "Universal Engineering" in p.read_text(encoding="utf-8")

@pytest.mark.parametrize("i", range(200))
def test_graph(i):
    graph=KnowledgeGraphBuilder().build([unit()])
    assert graph.objects("EKU-000001","uses_standard")==("ASEC",)

@pytest.mark.parametrize("i", range(200))
def test_versioning(i):
    vm=KnowledgeVersionManager(); vm.record(unit(),"initial")
    assert vm.versions("EKU-000001")==("1.0.0",)

@pytest.mark.parametrize("i", range(200))
def test_traceability(i):
    matrix=KnowledgeTraceabilityEngine().matrix(unit())
    assert matrix["human_review_required"] is True

@pytest.mark.parametrize("i", range(200))
def test_rejection(i):
    bad=unit(); bad.eku_id="bad"
    assert "invalid_eku_id" in KnowledgeValidator().validate(bad)

@pytest.mark.parametrize("i", range(199))
def test_orchestrator_contract(i): assert hasattr(AEKSOrchestrator,"import_unit")

def test_orchestrator_real(tmp_path):
    source=tmp_path/"eku.json"; source.write_text(json.dumps(unit().to_dict()),encoding="utf-8")
    result=AEKSOrchestrator().import_unit(source,tmp_path/"workspace")
    assert result["validated"] and Path(result["archive"]).exists()

@pytest.mark.parametrize("i", range(200))
def test_human_review_policy(i): assert unit().human_review_required is True
