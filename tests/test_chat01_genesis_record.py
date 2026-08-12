import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HISTORY=ROOT/"engineering/aias/history/chat01"

def test_chat01_source_is_integrity_and_limit_aware():
 data=json.loads((HISTORY/"CHAT01_SOURCE_MANIFEST.json").read_text(encoding="utf-8"));assert data["source"]["image_count"]==155;assert len(data["source"]["sha256"])==64;assert len(data["derived_corpus"]["sha256"])==64;assert data["authority_policy"]["historical_claims_of_completed installation_require_repository_evidence"] is True

def test_genesis_decisions_are_unique_classified_and_traceable():
 data=json.loads((HISTORY/"CHAT01_DECISION_REGISTER.json").read_text(encoding="utf-8"));rows=data["decisions"];ids=[row["id"] for row in rows];assert len(rows)>=20 and len(ids)==len(set(ids));assert all(row["evidence_sequences"] for row in rows);assert all(row["status"] in {"APPROVED","APPROVED_WITH_DESIGN_DETAILS_PENDING","INTERPRETATION"} for row in rows)

def test_gap_register_covers_every_approved_material_decision_without_inflation():
 decisions=json.loads((HISTORY/"CHAT01_DECISION_REGISTER.json").read_text(encoding="utf-8"))["decisions"];gap=json.loads((HISTORY/"CHAT01_MATERIALIZATION_GAP.json").read_text(encoding="utf-8"));expected={row["id"] for row in decisions if row["status"]!="INTERPRETATION"};actual={row["decision_id"] for row in gap["items"]};assert expected==actual;assert any(row["status"]=="NOT_EVIDENCED" for row in gap["items"]);assert any(row["status"]=="PARTIAL" for row in gap["items"])

def test_genesis_narrative_preserves_core_boundaries():
 text=(HISTORY/"AIAS_GENESIS_CHAT01.md").read_text(encoding="utf-8");assert "not merely another CAD" in text;assert "AutoCAD, Revit, ETABS" in text;assert "A download link or historical claim" in text;assert "AEC-000049" in text
