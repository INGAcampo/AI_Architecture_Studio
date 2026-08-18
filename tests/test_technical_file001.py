import json
from pathlib import Path
import zipfile
import pytest
from aias_technical_file import ProjectBrief,TechnicalFileGenerator
def brief():return ProjectBrief("LIGHTHOUSE-001","AIAS Lighthouse Reference Building","Bolivia - reference location","AIAS","Reference foundation engineering technical dossier","Structural")
def test_complete_real_technical_file_is_generated(tmp_path):
 result=TechnicalFileGenerator().generate(brief(),tmp_path/"file");assert result["complete"] and result["status"]=="FOR_REVIEW" and Path(result["archive"]).is_file() and len(result["sha256"])==64
 assert result["components"]["engineering"]["validated"] and result["components"]["drawings"]["validated"] and result["components"]["coordination"]["complete"]
def test_memory_pdf_manifest_and_handover_are_packaged(tmp_path):
 result=TechnicalFileGenerator().generate(brief(),tmp_path/"file");archive=Path(result["archive"])
 with zipfile.ZipFile(archive) as bundle:
  names=set(bundle.namelist());assert "descriptive_memory/MEMORIA_DESCRIPTIVA.pdf" in names and "INTEGRITY_MANIFEST.json" in names and any(x.startswith("handover/lifecycle_dossier/") for x in names)
 assert Path(result["components"]["descriptive_memory"]["pdf"]).read_bytes().startswith(b"%PDF-1.4")
def test_release_cannot_claim_construction_approval(tmp_path):
 result=TechnicalFileGenerator().generate(brief(),tmp_path/"file");assert result["professional_review_required"] and result["verified_official_jurisdiction_pack_required"] and result["status"]!="APPROVED_FOR_CONSTRUCTION"
def test_project_brief_requires_controlled_revision():
 with pytest.raises(ValueError,match="invalid_revision"):ProjectBrief("P","T","L","C","S","D","draft").validate()
