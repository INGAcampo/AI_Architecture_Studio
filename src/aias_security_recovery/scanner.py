"""Deterministic secret and unsafe-file scanner for recovery boundaries."""
from __future__ import annotations
import re
from pathlib import Path
from .policy import SecurityRecoveryPolicy

class SecurityScanner:
    """Detect excluded files, symlinks and likely embedded credentials."""
    PATTERNS=(re.compile(r"(?i)(api[_-]?key|password|private[_-]?key)\s*[:=]\s*['\"]?[^\s'\"]+"),re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"))
    def __init__(self,policy:SecurityRecoveryPolicy|None=None):self.policy=policy or SecurityRecoveryPolicy()
    def exclusion_reason(self,path:Path)->str|None:
        """Return the policy reason a file must not enter a backup."""
        name=path.name.lower()
        if path.is_symlink():return "symbolic_link"
        if name in self.policy.forbidden_names:return "forbidden_name"
        if path.suffix.lower() in self.policy.forbidden_suffixes:return "forbidden_suffix"
        return None
    def scan_text(self,text:str)->list[str]:
        """Return credential-pattern identifiers without exposing matched secrets."""
        return [f"secret_pattern:{index}" for index,pattern in enumerate(self.PATTERNS,1) if pattern.search(text)]
