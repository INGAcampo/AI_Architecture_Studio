from datetime import datetime,timedelta,timezone
import pytest
from aias_autonomous_cloud import *
def plane(tmp_path):
 p=AutonomousCloudControlPlane(tmp_path/"cloud.json");p.register_tenant(TenantQuota("TEN-AIAS",3,1,1000),{"PRINCIPAL-AIAS":("submit",)});p.register_tenant(TenantQuota("TEN-OTHER",3,1,1000),{"PRINCIPAL-OTHER":("submit",)});return p
def job(i,tenant="TEN-AIAS",priority=50):return CloudJob(f"JOB-{i}",tenant,"LIGHTHOUSE-001",("aeos",),{"command":"operate"},60,priority)
def test_tenant_authorization_and_queue_quota_are_enforced(tmp_path):
 p=plane(tmp_path);p.submit(job("1"),"PRINCIPAL-AIAS")
 with pytest.raises(ValueError,match="authorization_denied"):p.submit(job("2"),"PRINCIPAL-OTHER")
 p.submit(job("2"),"PRINCIPAL-AIAS");p.submit(job("3"),"PRINCIPAL-AIAS")
 with pytest.raises(ValueError,match="queued_job_quota"):p.submit(job("4"),"PRINCIPAL-AIAS")
def test_fair_capability_scheduler_and_concurrency(tmp_path):
 p=plane(tmp_path);p.submit(job("A1","TEN-AIAS",100),"PRINCIPAL-AIAS");p.submit(job("O1","TEN-OTHER",10),"PRINCIPAL-OTHER");worker=Worker("WRK-1",("aeos",));first=p.lease(worker);second=p.lease(Worker("WRK-2",("aeos",)));assert first["job_id"]=="JOB-A1" and second["tenant_id"]=="TEN-OTHER" and p.lease(Worker("WRK-3",("other",))) is None
def test_expired_lease_recovers_and_completion_requires_evidence(tmp_path):
 p=plane(tmp_path);p.submit(job("1"),"PRINCIPAL-AIAS");now=datetime.now(timezone.utc);leased=p.lease(Worker("WRK-1",("aeos",)),1,now);assert p.recover_expired(now+timedelta(seconds=2))==[leased["job_id"]];leased=p.lease(Worker("WRK-2",("aeos",)),60,now+timedelta(seconds=3))
 with pytest.raises(ValueError,match="completion_evidence"):p.complete(leased["job_id"],"WRK-2",[],{})
 result=p.complete(leased["job_id"],"WRK-2",[{"name":"result.zip","sha256":"a"*64}],{"validation":{"passed":True}});assert result["status"]=="COMPLETED" and result["attempt"]==2
def test_tenant_artifact_store_is_isolated_content_addressed_and_quota_bound(tmp_path):
 p=plane(tmp_path);store=TenantArtifactStore(tmp_path/"artifacts",p._quota);meta=store.put("TEN-AIAS","JOB-1","result.zip",b"engineering");assert store.get("TEN-AIAS",meta["sha256"])==b"engineering"
 with pytest.raises(ValueError,match="artifact_not_found"):store.get("TEN-OTHER",meta["sha256"])
 with pytest.raises(ValueError,match="unsafe_artifact_name"):store.put("TEN-AIAS","JOB-1","../secret",b"x")
def test_lighthouse_aeos_job_is_immediate_cloud_neutral_consumer(tmp_path):
 p=plane(tmp_path);p.submit(job("LIGHTHOUSE"),"PRINCIPAL-AIAS");leased=p.lease(Worker("WRK-AEOS",("aeos",)));store=TenantArtifactStore(tmp_path/"artifacts",p._quota);artifact=store.put("TEN-AIAS",leased["job_id"],"AEOS_RESULT.json",b'{"state":"OPERATING"}');result=p.complete(leased["job_id"],"WRK-AEOS",[artifact],{"validation":{"aeos_state":"OPERATING"}});assert result["status"]=="COMPLETED" and len(p.data["audit"][-1]["record_sha256"])==64
