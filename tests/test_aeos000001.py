from pathlib import Path
import pytest
from aias_engineering_os import EngineeringOperatingSystem,OperatingCommand,ServiceDescriptor,ServiceRegistry
from aias_engineering_os.bootstrap import load_services
from aias_central_nervous_system import Event,NervousSystemBus
ROOT=Path(__file__).resolve().parents[1];TOPOLOGY=ROOT/"engineering/aias/aeos/AEOS_SERVICE_TOPOLOGY.json"
def os(tmp_path,events=None):return EngineeringOperatingSystem(tmp_path/"aeos.json",load_services(TOPOLOGY),(events if events is not None else []).append)
def command(i,target,evidence):return OperatingCommand(f"CMD-{i}","LIGHTHOUSE-001",target,"AEOS",f"COR-{i}",evidence)
def test_service_topology_is_dependency_ready():
 registry=load_services(TOPOLOGY);assert len(registry.services)==7 and registry.platform_health()["ready"]
def test_complete_lighthouse_operating_cycle_is_evidence_gated_and_evented(tmp_path):
 events=[];system=os(tmp_path,events);system.initiate("LIGHTHOUSE-001","Lighthouse","CMD-0","COR-0");steps=[("PLANNED",{"portfolio_plan":"PMO-PLAN"},("PMO",)),("ASSIGNED",{"work_assignment":"VE-STRUCT-001"},("VIRTUAL_ORG",)),("PRODUCED",{"production_result":"TF-LIGHTHOUSE","validation":{"passed":True}},("DEV_PLATFORM","TECHNICAL_FILE")),("REVIEWED",{"independent_review":"VE-QA-001"},("VIRTUAL_ORG",)),("RELEASED",{"release":"LIGHTHOUSE-001_TECHNICAL_FILE_R00.zip","checksum":"sha256"},("TECHNICAL_FILE","SECURITY_RECOVERY")),("OPERATING",{"handover":"HANDOVER-ECP","monitoring_plan":"AIPD"},("CNS","PMO"))]
 for i,(target,evidence,services) in enumerate(steps,1):system.transition(command(i,target,evidence),services)
 assert system.status("LIGHTHOUSE-001")["state"]=="OPERATING" and len(events)==7 and len(system.status("LIGHTHOUSE-001")["history"])==7
def test_commands_are_idempotent_and_invalid_order_is_rejected(tmp_path):
 system=os(tmp_path);first=system.initiate("LIGHTHOUSE-001","Lighthouse","CMD-0","COR-0");assert system.initiate("LIGHTHOUSE-001","Lighthouse","CMD-0","COR-0")==first
 cmd=command(1,"PLANNED",{"portfolio_plan":"P"});system.transition(cmd,("PMO",));assert system.transition(cmd,("PMO",))["idempotent_replay"]
 with pytest.raises(ValueError,match="invalid_operating_transition"):system.transition(command(2,"RELEASED",{"release":"x","checksum":"y"}),("TECHNICAL_FILE",))
def test_unready_service_and_missing_gate_evidence_block_progress(tmp_path):
 registry=ServiceRegistry();registry.register(ServiceDescriptor("PMO","PMO","1",("planning",),(),"DEGRADED"));system=EngineeringOperatingSystem(tmp_path/"a.json",registry);system.initiate("LIGHTHOUSE-001","L","C0","X")
 with pytest.raises(ValueError,match="services_not_ready"):system.transition(command(1,"PLANNED",{"portfolio_plan":"P"}),("PMO",))
 system.services.services["PMO"]["health"]="READY"
 with pytest.raises(ValueError,match="missing_operating_evidence"):system.transition(command(2,"PLANNED",{}),("PMO",))
def test_real_cns_journal_is_an_immediate_event_consumer(tmp_path):
 bus=NervousSystemBus(tmp_path/"cns.json");sink=lambda row:bus.publish(Event.create(row.pop("type"),"AEOS",row,row.get("correlation_id")));system=EngineeringOperatingSystem(tmp_path/"aeos.json",load_services(TOPOLOGY),sink);system.initiate("LIGHTHOUSE-001","Lighthouse","CMD-0","COR-0");system.transition(command(1,"PLANNED",{"portfolio_plan":"PMO-PLAN"}),("PMO",));assert len(bus.journal.data["events"])==2 and bus.journal.data["events"][1]["event_type"]=="aeos.project.transitioned"
