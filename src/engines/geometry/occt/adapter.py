"""Stable AIAS-side contract for a future OCCT geometry backend."""

from __future__ import annotations

from dataclasses import dataclass

from .runtime_probe import OCCTRuntimeProbe, probe_occt_runtime


class OCCTUnavailableError(RuntimeError):
    """Raised when an OCCT-backed operation is requested without a runtime."""


@dataclass(frozen=True)
class OCCTGeometryAdapter:
    probe: OCCTRuntimeProbe

    @classmethod
    def discover(cls) -> "OCCTGeometryAdapter":
        return cls(probe=probe_occt_runtime())

    @property
    def available(self) -> bool:
        return self.probe.available

    def require_runtime(self) -> str:
        if not self.probe.available or not self.probe.selected_module:
            raise OCCTUnavailableError(
                "OCCT Python bindings are not available. "
                "Dependency bootstrap must pass before OCCT operations are enabled."
            )
        return self.probe.selected_module
