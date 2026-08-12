import json,zipfile
from pathlib import Path
from aias_lighthouse_project.brief import reference_brief
from aias_lighthouse_project.orchestrator import LighthouseOrchestrator
from aias_lighthouse_project.traceability import golden_thread
from aias_lighthouse_project.validation import validate
from aias_lighthouse_project.multistory import execute_reference_design,neutral_bim_ifc_export,reference_building
from aias_lighthouse_project.documentation import generate_structural_documents
def test_brief_is_reference_only_and_review_controlled():
 b=reference_brief();assert b["legal_status"]=="REFERENCE_ONLY" and b["professional_review_required"];assert b["jurisdiction_code"]=="VE" and b["jurisdiction_profile_id"]=="VE-001";assert b["normative_compliance_claimed"] is False and b["construction_approved"] is False
def test_golden_thread_is_complete():assert golden_thread()["complete"] and len(golden_thread()["links"])>=8
def test_validation_rejects_missing_artifacts():assert not validate([],reference_brief())["complete"]
def test_validation_never_grants_construction_approval():assert not validate([],reference_brief())["construction_approved"]
def test_vertical_slice_produces_engineering_dossier(tmp_path):
 r=LighthouseOrchestrator().execute(tmp_path);assert r["validated"] and r["artifacts"]>=9 and r["legal_status"]=="REFERENCE_ONLY"
def test_slice_contains_plan_calculation_and_descriptive_report(tmp_path):
 LighthouseOrchestrator().execute(tmp_path);d=tmp_path/"technical_dossier";assert (d/"drawings"/"foundation_plan.svg").is_file() and (d/"technical_file"/"foundation_documentation.json").is_file() and (d/"MEMORIA_DESCRIPTIVA.md").is_file() and (d/"JURISDICTION_CAPABILITY_MATRIX.json").is_file()
def test_release_is_versioned_and_readable(tmp_path):
 r=LighthouseOrchestrator().execute(tmp_path);assert len(r["sha256"])==64
 with zipfile.ZipFile(r["archive"]) as z:assert "MEMORIA_DESCRIPTIVA.md" in z.namelist() and "GOLDEN_THREAD.json" in z.namelist()
def test_venezuela_multistory_reference_closes_whole_building_loop():
 b=reference_building();assert b.validate()==[];assert len(b.nodes)==12 and len(b.members)==15;assert b.jurisdiction_pack_id=="VE-001"
 report=execute_reference_design();assert report["status"]=="FOR_PROFESSIONAL_REVIEW";assert report["model_summary"]=={"storeys":3,"bays":2,"nodes":12,"members":15};assert report["design"]["members"]==15;assert report["design"]["requiring_action"]==0;assert report["normative_compliance_claimed"] is False and report["construction_approved"] is False
def test_dossier_contains_whole_building_report(tmp_path):
 LighthouseOrchestrator().execute(tmp_path);report=json.loads((tmp_path/"technical_dossier"/"WHOLE_BUILDING_STRUCTURAL_REPORT.json").read_text(encoding="utf-8"));assert report["jurisdiction"]=="Venezuela";assert report["analysis"]["status"]=="COMPLETED";assert "REFERENCE_DEMANDS_NOT_NORMATIVE_ANALYSIS" in report["analysis"]["warnings"]
def test_reference_combinations_envelope_every_structural_member():
 report=execute_reference_design();envelopes=report["reference_load_envelopes"];assert envelopes["legal_status"]=="REFERENCE_ONLY_NOT_COVENIN";assert len(envelopes["combinations"])==3;assert len(envelopes["member_envelopes"])==15
def test_neutral_bim_export_contains_slabs_footings_columns_and_beams_without_losses():
 export=neutral_bim_ifc_export();kinds={row["kind"] for row in export["ifc_entities"]};assert {"IfcFooting","IfcSlab","IfcColumn","IfcBeam"}<=kinds;assert len(export["ifc_entities"])==21;assert export["losses"]==[];assert export["native_ifc_file_claimed"] is False and export["construction_approved"] is False
def test_dossier_contains_reference_combinations_and_neutral_ifc(tmp_path):
 LighthouseOrchestrator().execute(tmp_path);d=tmp_path/"technical_dossier";assert (d/"REFERENCE_LOAD_COMBINATIONS.json").is_file();assert (d/"WHOLE_BUILDING_BIM_IFC_NEUTRAL.json").is_file()
def test_whole_building_documents_are_coordinated_from_report(tmp_path):
 result=generate_structural_documents(tmp_path,execute_reference_design());assert result["drawings"]==2 and result["schedules"]==3;assert result["quantities"]["concrete_m3"]["total"]==30.282;assert result["construction_approved"] is False
 assert (tmp_path/"STRUCTURAL_PLAN.svg").is_file() and (tmp_path/"STRUCTURAL_ELEVATION.svg").is_file();assert len((tmp_path/"BEAM_SCHEDULE.csv").read_text().splitlines())==7;assert len((tmp_path/"COLUMN_SCHEDULE.csv").read_text().splitlines())==10
def test_release_contains_whole_building_documentation(tmp_path):
 LighthouseOrchestrator().execute(tmp_path);d=tmp_path/"technical_dossier"/"whole_building_documents";assert {"STRUCTURAL_PLAN.svg","STRUCTURAL_ELEVATION.svg","BEAM_SCHEDULE.csv","COLUMN_SCHEDULE.csv","FOUNDATION_SCHEDULE.csv","STRUCTURAL_QUANTITIES.json"}<={p.name for p in d.iterdir()}
