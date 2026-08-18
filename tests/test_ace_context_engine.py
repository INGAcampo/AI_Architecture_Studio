from __future__ import annotations

import json
from pathlib import Path

from aias_context_engine.builder import ContextBuilder
from aias_context_engine.storage import ContextStore
from aias_context_engine.validator import ContextValidator


def project(tmp_path: Path) -> Path:
    (tmp_path / "src" / "aias_demo").mkdir(parents=True)
    (tmp_path / "tests").mkdir()
    (tmp_path / "tests" / "test_demo.py").write_text("def test_demo(): assert True\n", encoding="utf-8")
    (tmp_path / "AIAS_AMP010C_ENGINEERING_OBJECT_KERNEL_INSTALLER").mkdir()
    (tmp_path / "AIAS_ECP000001C_FOUNDATION_CODE_CHECK_FRAMEWORK_INSTALLER").mkdir()
    return tmp_path


def test_builder_discovers_repository_state(tmp_path: Path):
    context = ContextBuilder(project(tmp_path)).build()
    assert context["identity"]["project_id"] == "AIAS"
    assert context["current_state"]["active_program"].startswith("ROADMAP-AUDIT-001")
    assert context["roadmap"]["next"].startswith("EXTERNAL-GATES-001")
    assert any(c["component_id"].startswith("AIAS_ECP000001C") for c in context["components"])


def test_context_is_integrity_valid(tmp_path: Path):
    context = ContextBuilder(project(tmp_path)).build()
    result = ContextValidator().validate(context)
    assert result["valid"], result["errors"]


def test_tampering_is_detected(tmp_path: Path):
    context = ContextBuilder(project(tmp_path)).build()
    context["roadmap"]["next"] = "UNAUTHORIZED"
    result = ContextValidator().validate(context)
    assert not result["valid"]
    assert "integrity checksum mismatch" in result["errors"]


def test_store_writes_master_snapshot_and_prompt(tmp_path: Path):
    root = project(tmp_path / "project")
    context = ContextBuilder(root).build()
    paths = ContextStore(root / "ACKC").write(context)
    assert Path(paths["master"]).exists()
    assert Path(paths["snapshot"]).exists()
    assert Path(paths["prompt"]).read_text(encoding="utf-8").startswith("# AIAS Continuity Prompt")
    assert Path(paths["project_state"]).exists()
    assert Path(paths["human_context"]).read_text(encoding="utf-8").startswith("# AIAS Master Context")
    assert json.loads(Path(paths["master"]).read_text(encoding="utf-8"))["schema_version"] == "1.0.0"


def test_required_permanent_rules_are_present(tmp_path: Path):
    context = ContextBuilder(project(tmp_path)).build()
    assert len(context["permanent_rules"]) >= 9
    assert any("macro-delivery" in rule for rule in context["permanent_rules"])
    assert any("AEC-000050" in rule for rule in context["permanent_rules"])
    assert any("AEC-000051" in rule for rule in context["permanent_rules"])
    assert any("AEC-000052" in rule for rule in context["permanent_rules"])


def test_builder_uses_versioned_master_plan_when_present(tmp_path: Path):
    root = project(tmp_path)
    plan = root / "engineering" / "aias" / "master" / "AIAS_MASTER_DEVELOPMENT_PLAN.json"
    plan.parent.mkdir(parents=True)
    plan.write_text('{"current":"W2-02 VALIDATED","next":"W2-03"}', encoding="utf-8")
    context = ContextBuilder(root).build()
    assert context["roadmap"]["current"] == "W2-02 VALIDATED"
    assert context["roadmap"]["next"] == "W2-03"
    assert context["current_state"]["active_program"] == "W2-02 VALIDATED"


def test_compliance_inventory_is_supported(tmp_path: Path):
    root = project(tmp_path)
    folder = root / "engineering" / "ace000001" / "compliance"
    folder.mkdir(parents=True)
    (folder / "QUALITY_GATES.json").write_text('{"component_id":"ACE-000001","all_passed":true,"gates":[{"gate_id":"QG-SPEC","passed":true}]}', encoding="utf-8")
    context = ContextBuilder(root).build()
    assert context["current_state"]["constitutional_compliance"]["ACE-000001"]["all_passed"]
