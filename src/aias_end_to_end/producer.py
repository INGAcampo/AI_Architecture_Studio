"""Lighthouse production orchestration from planning through operating custody."""
from __future__ import annotations
import hashlib,json,zipfile
from pathlib import Path
from aias_autonomous_cloud import AutonomousCloudControlPlane,CloudJob,TenantArtifactStore,TenantQuota,Worker
from aias_central_nervous_system import Event,NervousSystemBus
from aias_engineering_os import EngineeringOperatingSystem,OperatingCommand
from aias_engineering_os.bootstrap import load_services
from aias_security_recovery import BackupManager
from aias_technical_file import ProjectBrief,TechnicalFileGenerator
from aias_virtual_organization import VirtualEngineeringOrganization,WorkOrder
from aias_virtual_organization.bootstrap import load_roster

class EndToEndProjectProducer:
    """Coordinate real AIAS systems into one independently verifiable project release."""
    def __init__(self,project_root:Path):self.root=project_root
    def produce(self,brief:ProjectBrief,workspace:Path,signing_key:bytes)->dict:
        """Produce, review, operate, recover and cloud-package one reference project."""
        if len(signing_key)<32:raise ValueError("external_signing_key_required")
        workspace.mkdir(parents=True,exist_ok=True);bus=NervousSystemBus(workspace/"cns_journal.json")
        def sink(row):
            event_type=row.pop("type");bus.publish(Event.create(event_type,"AEOS",row,row.get("correlation_id")))
        aeos=EngineeringOperatingSystem(workspace/"aeos_state.json",load_services(self.root/"engineering/aias/aeos/AEOS_SERVICE_TOPOLOGY.json"),sink);organization=VirtualEngineeringOrganization(workspace/"virtual_org.json");load_roster(organization,self.root/"engineering/aias/virtual_organization/VIRTUAL_ENGINEER_ROSTER.json")
        aeos.initiate(brief.project_id,brief.title,"CMD-E2E-00","COR-E2E");self._transition(aeos,brief.project_id,"01","PLANNED",{"portfolio_plan":"PMO-LIGHTHOUSE-E2E"},("PMO",))
        work=organization.assign(WorkOrder("WO-E2E-001","Produce Lighthouse technical file",("technical_file",),"author","END-TO-END-001","HIGH",True));self._transition(aeos,brief.project_id,"02","ASSIGNED",{"work_assignment":work["assignee"]},("VIRTUAL_ORG",))
        technical=TechnicalFileGenerator().generate(brief,workspace/"production");organization.submit(work["work_id"],{"artifact":technical["archive"],"validation":{"complete":technical["complete"],"sha256":technical["sha256"]}});self._transition(aeos,brief.project_id,"03","PRODUCED",{"production_result":technical["technical_file_id"],"validation":{"complete":technical["complete"]}},("DEV_PLATFORM","TECHNICAL_FILE"))
        review=organization.assign_review(work["work_id"],"structural_review");reviewed=organization.complete_review(review["work_id"],"ACCEPT",{"review_report":"QA-E2E-001"});self._transition(aeos,brief.project_id,"04","REVIEWED",{"independent_review":review["assignee"]},("VIRTUAL_ORG",));self._transition(aeos,brief.project_id,"05","RELEASED",{"release":technical["archive"],"checksum":technical["sha256"]},("TECHNICAL_FILE","SECURITY_RECOVERY"))
        release_path=Path(technical["archive"]);backup=BackupManager().create(release_path.parent,workspace/"recovery"/"technical_release_backup.zip","SNP-E2E-001",signing_key);drill=BackupManager().drill(Path(backup["archive"]),workspace/"recovery"/"drill",signing_key);handover=technical["components"]["handover"]["handover_id"];self._transition(aeos,brief.project_id,"06","OPERATING",{"handover":handover,"monitoring_plan":"AIPD+LEVEL5_ASSURANCE"},("CNS","PMO"))
        cloud=AutonomousCloudControlPlane(workspace/"cloud_state.json");cloud.register_tenant(TenantQuota("TEN-AIAS",10,2,50_000_000),{"PRINCIPAL-AIAS":("submit",)});cloud.submit(CloudJob("JOB-E2E-LIGHTHOUSE","TEN-AIAS",brief.project_id,("aeos",),{"state":"OPERATING"},3600,100),"PRINCIPAL-AIAS");leased=cloud.lease(Worker("WRK-E2E-AEOS",("aeos",)));store=TenantArtifactStore(workspace/"cloud_artifacts",cloud._quota);artifact=store.put("TEN-AIAS",leased["job_id"],release_path.name,release_path.read_bytes());cloud_result=cloud.complete(leased["job_id"],"WRK-E2E-AEOS",[artifact],{"validation":{"aeos_state":"OPERATING","technical_file_sha256":technical["sha256"]}})
        result={"production_id":"E2E-LIGHTHOUSE-001","project_id":brief.project_id,"status":"OPERATING_REFERENCE_FOR_REVIEW","technical_file":technical,"virtual_work":{"author":work["assignee"],"reviewer":review["assignee"],"final_authority":reviewed["final_authority"]},"aeos":aeos.status(brief.project_id),"cns_events":len(bus.journal.data["events"]),"recovery":{"backup":backup,"drill":drill},"cloud":{"job_id":cloud_result["job_id"],"status":cloud_result["status"],"artifact":artifact},"professional_review_required":True,"audited_organizational_level":None};result["evidence_sha256"]=hashlib.sha256(json.dumps(result,sort_keys=True,separators=(",",":"),ensure_ascii=False,default=str).encode()).hexdigest();report=workspace/"END_TO_END_REPORT.json";report.write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str)+"\n",encoding="utf-8");archive=workspace/"release"/"END_TO_END_LIGHTHOUSE_001.zip";archive.parent.mkdir(exist_ok=True)
        with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as bundle:
            for path in sorted(workspace.rglob("*")):
                if path.is_file() and archive not in (path,) and archive.parent not in path.parents:bundle.write(path,path.relative_to(workspace))
        result["archive"]=str(archive);result["sha256"]=hashlib.sha256(archive.read_bytes()).hexdigest();report.write_text(json.dumps(result,ensure_ascii=False,indent=2,default=str)+"\n",encoding="utf-8");return result
    @staticmethod
    def _transition(aeos,project_id,index,target,evidence,services):return aeos.transition(OperatingCommand(f"CMD-E2E-{index}",project_id,target,"END-TO-END-001","COR-E2E",evidence),services)
