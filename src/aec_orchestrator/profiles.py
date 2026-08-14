from __future__ import annotations

from .contracts import AecApplication, WorkerCapability


DEFAULT_CAPABILITIES = {
    AecApplication.AUTOCAD: WorkerCapability(
        application=AecApplication.AUTOCAD,
        operations=(
            "probe_runtime",
            "open_drawing",
            "query_entities",
            "create_transient_entities",
        ),
    ),
    AecApplication.REVIT: WorkerCapability(
        application=AecApplication.REVIT,
        operations=(
            "probe_runtime",
            "open_model",
            "query_elements",
            "export_ifc",
        ),
    ),
    AecApplication.ETABS: WorkerCapability(
        application=AecApplication.ETABS,
        operations=(
            "probe_runtime",
            "open_model",
            "run_analysis",
            "read_results",
        ),
    ),
    AecApplication.SAP2000: WorkerCapability(
        application=AecApplication.SAP2000,
        operations=(
            "probe_runtime",
            "open_model",
            "run_analysis",
            "read_results",
        ),
    ),
    AecApplication.SAFE: WorkerCapability(
        application=AecApplication.SAFE,
        operations=(
            "probe_runtime",
            "open_model",
            "run_analysis",
            "read_results",
        ),
    ),
    AecApplication.GEO5: WorkerCapability(
        application=AecApplication.GEO5,
        operations=(
            "probe_runtime",
            "open_project",
            "run_analysis",
            "read_results",
        ),
    ),
}
