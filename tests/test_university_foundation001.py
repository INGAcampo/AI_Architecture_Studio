import json
from pathlib import Path
import pytest
from aias_university.catalog import UniversityCatalog
from aias_university import UniversityEngine,CredentialIssuer
ROOT=Path(__file__).resolve().parents[1];CAT=ROOT/"engineering/aias/university/AIAS_UNIVERSITY_CATALOG.json";INV=ROOT/"engineering/aias/master/inventory/AIAS_MASTER_CONCEPT_INVENTORY.json"
def setup():
 assets={x["id"] for x in json.loads(INV.read_text(encoding="utf-8"))["concepts"]};catalog=UniversityCatalog(CAT,assets);return catalog,UniversityEngine(catalog)
def test_catalog_links_real_assets_and_content():
 catalog,_=setup();course=catalog.get("COURSE-AIAS-FOUNDATIONS-001");assert len(course["capability_assets"])==5 and len(course["modules"])==3
def test_learning_assessment_and_credential_flow():
 catalog,engine=setup();cid="COURSE-AIAS-FOUNDATIONS-001";course=catalog.get(cid)
 for module in course["modules"]:
  for lesson in module["lessons"]:engine.complete_lesson("LEARNER-001",cid,lesson["lesson_id"])
 answers={q["question_id"]:q["correct_index"] for q in course["assessment"]["questions"]};assert engine.assess("LEARNER-001",cid,answers)["passed"]
 issuer=CredentialIssuer("AIAS-KNOWLEDGE-OFFICE",b"x"*32);credential=issuer.issue(engine,"LEARNER-001",cid,True);assert issuer.verify(credential) and credential["not_a_professional_license"]
def test_assessment_requires_content_completion():
 catalog,engine=setup();cid="COURSE-AIAS-FOUNDATIONS-001";answers={q["question_id"]:q["correct_index"] for q in catalog.get(cid)["assessment"]["questions"]}
 with pytest.raises(PermissionError):engine.assess("L",cid,answers)
def test_tampered_credential_is_rejected():
 catalog,engine=setup();cid="COURSE-AIAS-FOUNDATIONS-001"
 for module in catalog.get(cid)["modules"]:
  for lesson in module["lessons"]:engine.complete_lesson("L",cid,lesson["lesson_id"])
 engine.assess("L",cid,{q["question_id"]:q["correct_index"] for q in catalog.get(cid)["assessment"]["questions"]});issuer=CredentialIssuer("AIAS",b"y"*32);credential=issuer.issue(engine,"L",cid,True);credential["course_id"]="OTHER";assert not issuer.verify(credential)
