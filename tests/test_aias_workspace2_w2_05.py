from pathlib import Path
import json
import pytest

from gui.workspace import WorkspaceManager
from gui.workspace2 import LighthouseJourney, render_lighthouse_journey

ROOT=Path(__file__).resolve().parents[1]
DOSSIER=ROOT/"lighthouse000001_venezuela_outputs"/"technical_dossier"

def test_complete_reference_journey_is_evidence_backed_and_safe():
 data=LighthouseJourney(DOSSIER).inspect();assert len(data["stages"])==6;assert data["safe_reference_status"];assert data["golden_thread_complete"];assert data["stages"][-1]["status"]=="BLOCKED_EXTERNAL_AUTHORITY";assert len(data["evidence_sha256"])>=10;assert all(len(value)==64 for value in data["evidence_sha256"].values())

def test_stage_opens_real_documents_in_workspace(tmp_path):
 workspace=WorkspaceManager(tmp_path/"layouts");documents=LighthouseJourney(DOSSIER).open_stage("documentation",workspace);assert len(documents)==6;assert len(workspace.state.documents)==6;assert all(item.metadata["legal_status"]=="REFERENCE_ONLY" for item in documents)

def test_missing_or_unsafe_evidence_fails_closed(tmp_path):
 (tmp_path/"PROJECT_BRIEF.json").write_text(json.dumps({"construction_approved":True}),encoding="utf-8")
 with pytest.raises(FileNotFoundError,match="missing_lighthouse_evidence"):LighthouseJourney(tmp_path).inspect()

def test_renderer_exposes_reference_and_external_gates():
 output=render_lighthouse_journey(LighthouseJourney(DOSSIER).inspect());assert "<!doctype html>" in output;assert "REFERENCE ONLY" in output;assert "External authority gates remain visible" in output;assert "Venezuelan normative compliance claim" in output
