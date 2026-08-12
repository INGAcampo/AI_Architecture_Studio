from pathlib import Path
import pytest
from aias_virtual_organization import VirtualEngineer,VirtualEngineeringOrganization,WorkOrder
from aias_virtual_organization.bootstrap import load_roster
ROOT=Path(__file__).resolve().parents[1];ROSTER=ROOT/"engineering/aias/virtual_organization/VIRTUAL_ENGINEER_ROSTER.json"
def org(tmp_path):
 o=VirtualEngineeringOrganization(tmp_path/"organization.json");load_roster(o,ROSTER);return o
def test_roster_has_bounded_nonlicensed_credentialed_engineers(tmp_path):
 o=org(tmp_path);assert len(o.data["engineers"])==6 and all(not e["licensed_professional"] and e["credential_refs"] for e in o.data["engineers"].values())
 with pytest.raises(ValueError,match="cannot_be_licensed"):VirtualEngineer("VE-X","X","Role","OFFICE-1",("x",),("author",),("C",),licensed_professional=True).validate()
def test_technical_file_work_routes_by_competency_and_authority(tmp_path):
 o=org(tmp_path);row=o.assign(WorkOrder("WO-TF-001","Prepare Lighthouse technical file",("technical_file",),"author","TECHNICAL-FILE-001","HIGH",True));assert row["assignee"]=="VE-STRUCT-001"
 submitted=o.submit(row["work_id"],{"artifact":"LIGHTHOUSE-001_TECHNICAL_FILE_R00.zip","validation":{"passed":True}});assert submitted["human_professional_approval_required"]
def test_author_and_reviewer_are_segregated_and_human_retains_final_authority(tmp_path):
 o=org(tmp_path);row=o.assign(WorkOrder("WO-1","Foundation dossier",("technical_file",),"author","TF","HIGH",True));o.submit("WO-1",{"artifact":"file.zip","validation":{"passed":True}});review=o.assign_review("WO-1","structural_review");assert review["assignee"]!=row["assignee"]
 result=o.complete_review(review["work_id"],"ACCEPT",{"review_report":"QA-001"});assert result["status"]=="REVIEWED" and result["final_authority"]=="HUMAN_LICENSED_PROFESSIONAL"
def test_unqualified_or_unauthorized_work_is_rejected(tmp_path):
 o=org(tmp_path)
 with pytest.raises(ValueError,match="no_authorized"):o.assign(WorkOrder("WO-X","Unknown",("nuclear",),"approve","X","CRITICAL",True))
