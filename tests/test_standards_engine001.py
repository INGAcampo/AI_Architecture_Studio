import json
from datetime import date
from pathlib import Path
import pytest
from aias_standards_engine import StandardsEngine, StandardsPackage
ROOT=Path(__file__).resolve().parents[1]
def test_standards_engine_requires_explicit_jurisdiction_and_version():
    engine=StandardsEngine(); engine.register(StandardsPackage("pkg-ve","VE","0.1.0",date(2026,1,1),"source"))
    result=engine.check("pkg-ve","beam.flexure",{"Mu":10})
    assert result["evaluated"] is False and result["professional_review_required"] is True
def test_duplicate_packages_fail_closed():
    engine=StandardsEngine(); p=StandardsPackage("pkg","VE","1") ; engine.register(p)
    with pytest.raises(ValueError,match="duplicate_standards_package"): engine.register(p)
def test_venezuela_package_is_shell_only():
    spec=json.loads((ROOT/"engineering/aias/standards_engine/packages/VE/PACKAGE.json").read_text(encoding="utf-8"))
    assert spec["licensed_source_verified"] is False and spec["status"] == "SHELL_ONLY_NOT_FOR_COMPLIANCE"
