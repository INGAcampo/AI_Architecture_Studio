"""Reinforcement detailing with explicit fail-closed design outcome semantics."""
from __future__ import annotations

from .engine_legacy import ReinforcementEngine as _LegacyReinforcementEngine
from .engine_legacy import ReinforcementModel, sha


class ReinforcementEngine(_LegacyReinforcementEngine):
    """Preserve legacy detailing while distinguishing capacity failure from missing evidence."""

    def build(self, structural_result, standards_evidence: dict, project_id="PILOT-BUILDING-001") -> ReinforcementModel:
        status = getattr(structural_result, "status", None)
        if status == "FAIL":
            checks = getattr(structural_result, "design_checks", {}) or {}
            failed = [
                element_id
                for element_id, check in checks.items()
                if check.get("status") == "FAIL"
            ]
            if failed:
                raise ValueError(
                    "DESIGN_CAPACITY_EXCEEDED: structural demand exceeds capacity for "
                    + ",".join(sorted(failed))
                )
        return super().build(structural_result, standards_evidence, project_id=project_id)


__all__ = ["ReinforcementEngine", "ReinforcementModel", "sha"]
