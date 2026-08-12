import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_web_spec_and_public_registry_are_truthful():
    spec = json.loads((ROOT / "engineering/aias/experience/EXP_WEB_001_SPEC.json").read_text(encoding="utf-8"))
    registry = json.loads((ROOT / "sites/aias-official/public/capabilities.json").read_text(encoding="utf-8"))
    assert spec["status"] == "LOCAL_BUILD_VALIDATED_DEPLOYMENT_APPROVAL_PENDING"
    assert spec["evidence"]["external_deployment_performed"] is False
    serialized = json.dumps(registry, ensure_ascii=False).lower()
    assert "venezuela" in serialized
    assert "not_available_licensed_rules_pending" in serialized
    assert "not_authorized" in serialized


def test_web_has_required_professional_surfaces_and_metadata():
    page = (ROOT / "sites/aias-official/app/page.tsx").read_text(encoding="utf-8")
    layout = (ROOT / "sites/aias-official/app/layout.tsx").read_text(encoding="utf-8")
    for required in ("TRUST CENTER", "AIAS UNIVERSITY", "const disciplines", "CAPACIDADES VERIFICADAS"):
        assert required in page
    assert "/og.png" in layout
    assert "AI Architecture Studio" in layout


def test_dependency_build_scripts_are_explicitly_allowlisted():
    policy = (ROOT / "sites/aias-official/pnpm-workspace.yaml").read_text(encoding="utf-8")
    assert "dangerouslyAllowAllBuilds" not in policy
    for package in ("esbuild", "sharp", "unrs-resolver", "workerd"):
        assert f"{package}: true" in policy
