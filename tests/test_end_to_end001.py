from pathlib import Path
import pytest
from aias_end_to_end import EndToEndProjectProducer
from aias_technical_file import ProjectBrief
ROOT=Path(__file__).resolve().parents[1];KEY=b"end-to-end-test-key-material-0001"
def brief():return ProjectBrief("LIGHTHOUSE-001","AIAS Lighthouse Reference Building","Bolivia - reference location","AIAS","End-to-end reference foundation project","Structural")
def test_complete_lighthouse_project_reaches_operating_with_all_evidence(tmp_path):
 result=EndToEndProjectProducer(ROOT).produce(brief(),tmp_path/"e2e",KEY);assert result["status"]=="OPERATING_REFERENCE_FOR_REVIEW" and result["aeos"]["state"]=="OPERATING" and result["technical_file"]["complete"] and result["cloud"]["status"]=="COMPLETED" and result["recovery"]["drill"]["verified"] and result["cns_events"]==7
 assert result["virtual_work"]["author"]!=result["virtual_work"]["reviewer"] and result["virtual_work"]["final_authority"]=="HUMAN_LICENSED_PROFESSIONAL" and Path(result["archive"]).is_file()
def test_end_to_end_never_claims_professional_or_audited_level5_approval(tmp_path):
 result=EndToEndProjectProducer(ROOT).produce(brief(),tmp_path/"e2e",KEY);assert result["professional_review_required"] and result["audited_organizational_level"] is None and "APPROVED_FOR_CONSTRUCTION" not in result["status"]
def test_external_signing_key_is_required(tmp_path):
 with pytest.raises(ValueError,match="external_signing_key_required"):EndToEndProjectProducer(ROOT).produce(brief(),tmp_path/"e2e",b"short")
