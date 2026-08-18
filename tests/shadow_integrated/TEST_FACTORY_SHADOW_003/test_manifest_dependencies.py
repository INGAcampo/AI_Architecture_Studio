import hashlib

from shadow_test_factory_verify.manifest_verify import verify_manifest_entries
from shadow_test_factory_verify.dependencies import validate_dependency_order


def test_manifest_verification_detects_valid_file(tmp_path):
    file_path=tmp_path/"a.txt"
    file_path.write_text("AIAS",encoding="ascii")
    digest=hashlib.sha256(b"AIAS").hexdigest()

    result=verify_manifest_entries(
        tmp_path,
        ({"path":"a.txt","sha256":digest},),
    )
    assert result.passed is True


def test_manifest_verification_detects_tamper(tmp_path):
    file_path=tmp_path/"a.txt"
    file_path.write_text("AIAS",encoding="ascii")

    result=verify_manifest_entries(
        tmp_path,
        ({"path":"a.txt","sha256":"0"*64},),
    )
    assert result.passed is False
    assert result.mismatched==("a.txt",)


def test_dependency_order_accepts_parent_before_child():
    result=validate_dependency_order(
        (
            {"megablock":"A","dependency":""},
            {"megablock":"B","dependency":"A"},
            {"megablock":"C","dependency":"B"},
        )
    )
    assert result.passed is True


def test_dependency_order_rejects_missing_parent():
    result=validate_dependency_order(
        (
            {"megablock":"B","dependency":"A"},
        )
    )
    assert result.passed is False
    assert "missing dependency" in result.violations[0]
