import json
from pathlib import Path
from aias_aeks.models import KnowledgeUnit
from aias_engineering_intelligence import *
from aias_engineering_intelligence.reference import assess_bearing_pressure
from aias_enterprise_knowledge_graph import Edge,EnterpriseKnowledgeGraph,Node
ROOT=Path(__file__).resolve().parents[1]
def evidence(i,claim,value,trust=1):return Evidence(i,"TEST","test",claim,value,trust,"a"*64)
def request(risk="MEDIUM",regulated=False):return IntelligenceRequest("REQ-I","Question",("a","b"),risk,regulated,"CTX")
def test_complete_consistent_evidence_can_recommend_with_audit():
 core=EngineeringIntelligenceCore();result=core.recommend(request(),[evidence("E1","a",1,.9),evidence("E2","b",2,.9)],"Proceed");assert result.status=="RECOMMEND" and result.confidence==.9 and len(core.audit[0]["record_sha256"])==64
def test_missing_or_conflicting_evidence_forces_abstention():
 core=EngineeringIntelligenceCore();missing=core.recommend(request(),[evidence("E1","a",1)],"Proceed");assert missing.status=="ABSTAIN" and "missing_claims:b" in missing.reasons
 conflict=core.recommend(request(),[evidence("E1","a",1),evidence("E2","a",2),evidence("E3","b",3)],"Proceed");assert conflict.status=="ABSTAIN" and any(x.startswith("conflicting_claims") for x in conflict.reasons)
def test_high_risk_recommendation_never_becomes_professional_approval():
 result=EngineeringIntelligenceCore().recommend(request("HIGH",True),[evidence("E1","a",1,.95),evidence("E2","b",2,.95)],"Use result");assert result.status=="RECOMMEND" and result.professional_review_required and result.final_authority=="HUMAN_LICENSED_PROFESSIONAL"
def test_real_aeks_differential_and_ekg_consumer(tmp_path):
 unit=KnowledgeUnit(**json.loads((ROOT/"engineering/aias/aeks/EKU-000002-bearing-pressure.json").read_text()));graph=EnterpriseKnowledgeGraph(tmp_path/"g.json");graph.add_node(Node("SYS-000005","SYSTEM","AEKS",provenance={"source":"AMIR"}));graph.add_node(Node("ENG-000004","CAPABILITY","Foundation",provenance={"source":"AMIR"}));graph.add_edge(Edge("E","SYS-000005","enables","ENG-000004",provenance={"source":"AMIR"}));result,execution,diff=assess_bearing_pressure(EngineeringIntelligenceCore(),unit,graph,{"vertical_load_kn":800.0,"area_m2":5.0});assert result.status=="RECOMMEND" and execution["output"]["value"]==160 and diff["passed"] and result.professional_review_required
