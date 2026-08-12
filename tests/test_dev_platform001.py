import json
from pathlib import Path
import pytest
from aias_development_platform import DevelopmentJob,DevelopmentPlatform,DevelopmentPolicy
def spec(tmp_path,payload):
 p=tmp_path/"spec.json";p.write_text(json.dumps({"id":"SPEC-X","version":"1.0.0",**payload}),encoding="utf-8");return p
def test_policy_selects_least_complex_capable_engine(tmp_path):
 policy=DevelopmentPolicy();assert policy.select({})=="v3" and policy.select({"template_id":"T"})=="v4" and policy.select({"autonomous":True})=="v5" and policy.select({},"v5")=="v5"
def test_platform_normalizes_certification_evidence_and_events(tmp_path):
 events=[];runners={"v3":lambda s,w:{"certified":True,"artifacts":[w/"module.py"],"traceability":1.0},"v4":lambda s,w:{},"v5":lambda s,w:{}}
 job=DevelopmentJob("JOB-1",spec(tmp_path,{}),tmp_path/"work/JOB-1",correlation_id="COR-1");result=DevelopmentPlatform(tmp_path/"work",runners,events.append).execute(job)
 assert result.engine=="v3" and result.certified and len(result.evidence["development_platform"]["evidence_sha256"])==64 and [e["type"] for e in events]==["development.started","development.completed"]
def test_advanced_and_autonomous_selection_are_executable(tmp_path):
 runners={k:(lambda s,w,k=k:{"certified":True,"artifacts":[],"selected":k}) for k in ("v3","v4","v5")};platform=DevelopmentPlatform(tmp_path/"runs",runners)
 a=platform.execute(DevelopmentJob("J4",spec(tmp_path,{"transactional":True}),tmp_path/"runs/J4",correlation_id="C4"));assert a.engine=="v4"
 b=platform.execute(DevelopmentJob("J5",spec(tmp_path,{"domains":["BIM"]}),tmp_path/"runs/J5",correlation_id="C5"));assert b.engine=="v5"
def test_job_identity_specification_and_workspace_boundaries_are_enforced(tmp_path):
 platform=DevelopmentPlatform(tmp_path/"runs",{"v3":lambda s,w:{},"v4":lambda s,w:{},"v5":lambda s,w:{}});p=spec(tmp_path,{})
 with pytest.raises(ValueError,match="missing_job_identity"):platform.execute(DevelopmentJob("J",p,tmp_path/"runs/J",correlation_id=""))
 with pytest.raises(ValueError,match="workspace_outside"):platform.execute(DevelopmentJob("J",p,tmp_path/"outside",correlation_id="C"))
def test_real_v3_engine_is_an_immediate_consumer(tmp_path):
 payload={"id":"SPEC-993501","title":"Platform consumer","module_name":"platform_generated","requirements":[{"id":"REQ-993501","statement":"Generate governed code.","acceptance_criteria":["Code exists."]}],"dependencies":[],"architecture_refs":["ARCH-DEV-PLATFORM-001"],"adr_refs":["ADR-DEV-PLATFORM-001"]}
 result=DevelopmentPlatform(tmp_path/"runs").execute(DevelopmentJob("JOB-REAL",spec(tmp_path,payload),tmp_path/"runs/JOB-REAL",correlation_id="COR-REAL"))
 assert result.engine=="v3" and result.certified and result.evidence["release"]["archive"].endswith(".zip")
