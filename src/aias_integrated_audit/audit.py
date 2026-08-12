from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
@dataclass(frozen=True, slots=True)
class AuditReport:
    checked: int
    present: int
    missing: tuple[str, ...]
    external_pending: tuple[str, ...]
    status: str
class IntegratedAudit:
    def run(self, root: Path, artifacts: tuple[str, ...], external_pending: tuple[str, ...]) -> AuditReport:
        missing=tuple(path for path in artifacts if not (root/path).exists())
        status="LOCAL_CONTRACTS_VALID_EXTERNAL_GATES_PENDING" if not missing else "INCOMPLETE_ARTIFACTS"
        return AuditReport(len(artifacts),len(artifacts)-len(missing),missing,external_pending,status)
