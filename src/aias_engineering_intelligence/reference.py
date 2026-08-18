"""Real AEKS, differential-validation and EKG-backed reference assessment."""
from __future__ import annotations
import hashlib,json
from aias_engineering_wave12 import DifferentialValidator
from aias_executable_knowledge import DeclarativeKnowledgeExecutor
from .models import Evidence,IntelligenceRequest

def assess_bearing_pressure(core,knowledge_unit,graph,inputs:dict,baseline_value:float=160.0):
    """Execute admitted knowledge and recommend only when baseline and graph context agree."""
    execution=DeclarativeKnowledgeExecutor().execute(knowledge_unit,inputs,"CALC-BEARING-001");value=execution["output"]["value"];diff=DifferentialValidator().compare({"values":{"q":baseline_value},"units":{"q":"kPa"},"provenance":"REF-FOUND-001"},{"values":{"q":value},"units":{"q":"kPa"},"provenance":execution["evidence_sha256"]},.01,.001);context=graph.related("SYS-000005","both") if "SYS-000005" in graph.data["nodes"] else []
    raw=[("EVD-AEKS","calculated_pressure",value,1.0,execution["evidence_sha256"],{"execution":execution}),("EVD-DIFF","baseline_agreement",diff["passed"],.95,digest(diff),{"differential":diff}),("EVD-EKG","knowledge_context_present",bool(context),.9,digest(context),{"edges":context})];evidence=[Evidence(i,t,"AIAS",claim,value,trust,sha,"REFERENCE_ONLY",meta) for (i,claim,value,trust,sha,meta),(t) in zip(raw,("EXECUTION","DIFFERENTIAL","GRAPH"))]
    request=IntelligenceRequest("INT-FOUND-001","Is the reference bearing-pressure calculation consistent with governed evidence?",("calculated_pressure","baseline_agreement","knowledge_context_present"),"HIGH",True,"LIGHTHOUSE-001");return core.recommend(request,evidence,"Recommend the calculated reference bearing pressure for licensed professional review."),execution,diff
def digest(value):
    """Return a deterministic digest for reference evidence."""
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()
