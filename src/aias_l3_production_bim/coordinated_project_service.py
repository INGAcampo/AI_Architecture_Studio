"""003D project service integrating native coordination and QA/QC."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from .professional_publication_service import (
    ProfessionalPublicationProjectService,
)
from .native_coordination import NativeCoordinationBridge


class CoordinatedProductionProjectService(ProfessionalPublicationProjectService):
    """Extend certified professional-documentation flow with coordination."""

    def __init__(
        self,
        project_name: str,
        *,
        discovery_path: Path,
        drawing_viewer: Any | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            project_name,
            discovery_path=discovery_path,
            drawing_viewer=drawing_viewer,
            **kwargs,
        )
        self.coordination = NativeCoordinationBridge()

    def workspace_projection_with_coordination(self) -> dict[str, Any]:
        """Extend Workspace 2 projection with coordination/QA inventory."""
        base = self.workspace_projection_with_publication()
        snap = self.coordination.snapshot()

        return {
            **base,
            "multidisciplinary_coordination": {
                "federated_models": snap.federated_models,
                "issues": snap.issues,
                "revisioned_objects": snap.revisioned_objects,
                "clash_runs": snap.clash_runs,
                "validation_runs": snap.validation_runs,
                "quality_runs": snap.quality_runs,
                "boq_runs": snap.boq_runs,
                "ifc_runs": snap.ifc_runs,
                "delivery_manifests": snap.delivery_manifests,
            },
        }
