from __future__ import annotations
import hashlib
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class IntegrityResult:
    passed:bool
    expected_sha256:str
    actual_sha256:str|None

def verify_file_hash(path,expected_sha256:str)->IntegrityResult:
    p=Path(path)
    if len(expected_sha256)!=64:
        raise ValueError("expected_sha256 must be SHA256")
    if not p.is_file():
        return IntegrityResult(False,expected_sha256,None)
    actual=hashlib.sha256(p.read_bytes()).hexdigest()
    return IntegrityResult(actual==expected_sha256,expected_sha256,actual)
