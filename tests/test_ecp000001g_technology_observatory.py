import json
from aias_foundation_handover.orchestrator import FoundationHandoverOrchestrator
from aias_technology_observatory.catalog import initial_observations
from aias_technology_observatory.engine import TechnologyObservatoryEngine
from aias_technology_observatory.governance import evaluate
from aias_technology_observatory.materialization import earliest_action
from aias_technology_observatory.orchestrator import TechnologyObservatoryOrchestrator
from aias_technology_observatory.scoring import score

def dossier(tmp_path):
 p=tmp_path/"f";FoundationHandoverOrchestrator().execute(p);return p/"lifecycle_dossier"/"FOUNDATION_HANDOVER_DOSSIER.json"
def test_catalog_has_authoritative_sources():assert all(o.source_url.startswith("https://") and o.publisher for o in initial_observations())
def test_score_identifies_giant_step():assert score(.95,.9,.9,.8,.2,1)["giant_step"]
def test_invalid_score_rejected():
 import pytest
 with pytest.raises(ValueError):score(2,1,1,1,0,1)
def test_constitutional_filter_accepts_safe_reference():assert evaluate(True,True,True,True,"CONDITIONAL_REFERENCE_ONLY")["accepted"]
def test_constitutional_filter_blocks_incompatible():assert not evaluate(True,True,True,False,"PASSED")["accepted"]
def test_aec49_emits_immediate_action():assert earliest_action("X",True,True)["action"]=="IMPLEMENT_REFERENCE_ADAPTER"
def test_engine_consumes_ecpf(tmp_path):
 r=TechnologyObservatoryEngine().analyze(initial_observations()[0],dossier(tmp_path),{"relevance":.9,"impact":.9,"reuse":.8,"acceleration":.8,"risk":.2});assert r["consumer_context"]["maturity_level"]==5
def test_orchestrator_materializes_portfolio(tmp_path):
 r=TechnologyObservatoryOrchestrator().execute(tmp_path/"ato");p=tmp_path/"ato"/"observatory"/"ATO_OPPORTUNITY_PORTFOLIO.json";adapter=tmp_path/"ato"/"observatory"/"ATO_NIST_AIRMF_ADAPTER.json";assert r["validated"] and r["immediate_actions"]==3 and json.loads(p.read_text())["governing_article"]=="AEC-000049" and json.loads(adapter.read_text())["status"]=="MATERIALIZED_REFERENCE_CAPABILITY"
