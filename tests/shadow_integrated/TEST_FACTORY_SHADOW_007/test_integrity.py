import hashlib
from shadow_test_factory_integrity.integrity import verify_file_hash

def test_valid_file_hash_passes(tmp_path):
    p=tmp_path/"a.txt"
    p.write_text("AIAS",encoding="ascii")
    expected=hashlib.sha256(b"AIAS").hexdigest()
    assert verify_file_hash(p,expected).passed is True

def test_tampered_file_hash_fails(tmp_path):
    p=tmp_path/"a.txt"
    p.write_text("AIAS",encoding="ascii")
    assert verify_file_hash(p,"0"*64).passed is False

def test_missing_file_fails_without_exception(tmp_path):
    r=verify_file_hash(tmp_path/"missing.txt","0"*64)
    assert r.passed is False
    assert r.actual_sha256 is None
