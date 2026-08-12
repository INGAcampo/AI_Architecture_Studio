from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable
@dataclass(frozen=True, slots=True)
class ReconciliationResult:
    checked: int
    present: tuple[str, ...]
    missing: tuple[str, ...]
    external_pending: tuple[str, ...]
    valid: bool
class RoadmapReconciler:
    def reconcile(self, root: Path, artifacts: Iterable[str], external_pending: Iterable[str] = ()) -> ReconciliationResult:
        paths=tuple(artifacts); present=tuple(p for p in paths if (root/p).exists()); missing=tuple(p for p in paths if not (root/p).exists())
        return ReconciliationResult(len(paths),present,missing,tuple(external_pending),not missing)
