"""AIAS optional OCCT integration namespace."""

from .runtime_probe import OCCTRuntimeProbe, probe_occt_runtime
from .adapter import OCCTGeometryAdapter, OCCTUnavailableError

__all__ = [
    "OCCTRuntimeProbe",
    "probe_occt_runtime",
    "OCCTGeometryAdapter",
    "OCCTUnavailableError",
]
