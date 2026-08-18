from aias_governance_assurance.assets import validate_asset
from aias_governance_assurance.decisions import registry
from aias_governance_assurance.documentation import audit, audit_packages, require_documented_packages
from aias_governance_assurance.dod import REQUIRED,evaluate
from aias_governance_assurance.orchestrator import GovernanceAssuranceOrchestrator
from aias_governance_assurance.sdd import audit_compliance

def test_recovered_decisions_have_provenance_and_evidence():assert len(registry())>=25 and all(r["captures"] and r["evidence"] for r in registry())
def test_binding_and_roadmap_are_distinguished():assert {r["classification"] for r in registry()}=={"BINDING","ROADMAP"}
def test_asset_lifecycle_accepts_valid_asset():assert validate_asset({"id":"AEC-000049","version":"1.0.0","status":"VALIDATED"})==[]
def test_asset_lifecycle_rejects_invalid_fields():assert len(validate_asset({"id":"bad","version":"1","status":"DONE"}))==3
def test_dod_requires_all_evidence():assert not evaluate({})["done"] and set(evaluate({})["missing"])==set(REQUIRED)
def test_dod_accepts_complete_evidence():assert evaluate({k:True for k in REQUIRED})["done"]
def test_documentation_audit_is_evidence_based(tmp_path):
 p=tmp_path/"src"/"aias_demo";p.mkdir(parents=True);(p/"a.py").write_text('"""module"""\ndef public():\n pass\n');r=audit(tmp_path);assert r["module_coverage"]==1 and r["public_symbol_coverage"]==0
def test_documentation_audit_includes_public_methods(tmp_path):
 p=tmp_path/"src"/"aias_demo";p.mkdir(parents=True);(p/"a.py").write_text('"""module"""\nclass API:\n """public class"""\n def operation(self):\n  return 1\n');r=audit(tmp_path);assert r["public_symbols"]==2 and any(x.get("symbol")=="API.operation" for x in r["missing"])
def test_sdd_audit_requires_complete_pack(tmp_path):
 p=tmp_path/"engineering"/"demo"/"compliance";p.mkdir(parents=True);r=audit_compliance(tmp_path);assert not r["all_complete"]
def test_orchestrator_generates_honest_baseline(tmp_path):
 root=tmp_path/"repo";(root/"src"/"aias_demo").mkdir(parents=True);(root/"src"/"aias_demo"/"x.py").write_text('def x():\n return 1\n');r=GovernanceAssuranceOrchestrator().execute(root,tmp_path/"out");assert r["validated"] and r["module_doc_coverage"]==0 and (tmp_path/"out"/"ALIGNMENT_BACKLOG.json").is_file()

def test_active_high_risk_packages_pass_documentation_gate():
 root=__import__('pathlib').Path(__file__).resolve().parents[1];packages=("aias_foundation_handover","aias_technology_observatory","aias_governance_assurance");assert audit_packages(root,packages)["all_complete"];require_documented_packages(root,packages)
