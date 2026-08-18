"""Native multidisciplinary coordination bridge for L3 Production BIM 003D."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from engines.structural.collaboration import BimCollaborationManager
from engines.structural.clashes import ClashDetector
from aias_foundation_code_checks.validation import CodeCheckValidator
from aias_aeps_governance_sdd.quality import QualityGateEngine
from aias_foundation_delivery.issues import IssueRegister
from aias_foundation_delivery.models import CoordinationIssue, IssueStatus
from aias_engineering_object.versioning import VersionStore
from aias_omega_release6.cost import BoqEngine
from aias_cad_bim_integration.ifc_sync import NeutralIfcSynchronizer
from aias_foundation_delivery.revisions import create_revision_manifest


class CoordinationContractError(RuntimeError):
    """Raised when an exact coordination contract is used incorrectly."""


@dataclass(slots=True)
class CoordinationSnapshot:
    """Summarize native multidisciplinary coordination activity and inventory."""

    federated_models: int
    issues: int
    revisioned_objects: int
    clash_runs: int
    validation_runs: int
    quality_runs: int
    boq_runs: int
    ifc_runs: int
    delivery_manifests: int


class NativeCoordinationBridge:
    """Exact adapters over repository coordination / QA / delivery authorities."""

    def __init__(self) -> None:
        self.collaboration = BimCollaborationManager()
        self.clashes = ClashDetector()
        self.validation = CodeCheckValidator()
        self.quality = QualityGateEngine()
        self.issues = IssueRegister()
        self.versions = VersionStore()
        self.boq = BoqEngine()
        self.ifc = NeutralIfcSynchronizer()

        self._clash_runs: list[Any] = []
        self._validation_runs: list[Any] = []
        self._quality_runs: list[Any] = []
        self._boq_runs: list[Any] = []
        self._ifc_runs: list[Any] = []
        self._delivery_manifests: list[Any] = []

    def register_federated_model(self, model: Any) -> Any:
        """Register a native FederatedModel through the exact manager."""
        return self.collaboration.register(model)

    def federated_models(self) -> Any:
        """Return all native federated models currently registered."""
        return self.collaboration.federated_models()

    def models_by_discipline(self, discipline: Any) -> Any:
        """Return registered federated models belonging to a discipline."""
        return self.collaboration.by_discipline(discipline)

    def latest_federated_revision(self) -> Any:
        """Return the latest revision known by the collaboration authority."""
        return self.collaboration.latest_revision()

    def detect_clash(
        self,
        first_id: str,
        first_box: Any,
        second_id: str,
        second_box: Any,
    ) -> Any:
        """Run exact clash detection with native bounding-box compatible objects."""
        result = self.clashes.detect(
            first_id,
            first_box,
            second_id,
            second_box,
        )
        self._clash_runs.append(result)
        return result

    def boxes_intersect(
        self,
        first_box: Any,
        second_box: Any,
        *,
        clearance: float = 0.0,
    ) -> bool:
        """Test whether two native clash boxes intersect at a clearance."""
        return bool(
            self.clashes.intersects(
                first_box,
                second_box,
                clearance=float(clearance),
            )
        )

    def validate_design_input(self, data: Any) -> list[str]:
        """Validate a native design input and return validation errors."""
        result = self.validation.validate_input(data)
        self._validation_runs.append(result)
        return result

    def validate_code_pack(self, pack: Any) -> list[str]:
        """Validate a native code pack and return validation errors."""
        result = self.validation.validate_pack(pack)
        self._validation_runs.append(result)
        return result

    def evaluate_quality(self, specification: Any, traceability: Any) -> Any:
        """Evaluate native QA/QC gates for specification traceability."""
        result = self.quality.evaluate(specification, traceability)
        self._quality_runs.append(result)
        return result

    def quality_passed(self, specification: Any, traceability: Any) -> bool:
        """Return whether native QA/QC gates pass for supplied inputs."""
        return bool(self.quality.passed(specification, traceability))

    def add_issue(
        self,
        *,
        issue_id: str,
        title: str,
        description: str,
        owner: str,
        status: IssueStatus = IssueStatus.OPEN,
        resolution: str | None = None,
    ) -> CoordinationIssue:
        """Create and register a native multidisciplinary coordination issue."""
        issue = CoordinationIssue(
            issue_id=issue_id,
            title=title,
            description=description,
            owner=owner,
            status=status,
            resolution=resolution,
        )
        self.issues.add(issue)
        return issue

    def resolve_issue(self, issue_id: str, resolution: str) -> Any:
        """Resolve a registered coordination issue through the native register."""
        return self.issues.resolve(issue_id, resolution)

    def snapshot_revision(self, engineering_object: Any, note: str) -> None:
        """Store a native version snapshot for an engineering object."""
        self.versions.snapshot(engineering_object, note)

    def revision_count(self, object_id: str) -> int:
        """Return the number of native snapshots stored for an object."""
        return self.versions.revisions(object_id)

    def build_boq(self, project: Any, catalog: Any) -> Any:
        """Build a native bill of quantities from a BIM project and catalog."""
        result = self.boq.from_bim(project, catalog)
        self._boq_runs.append(result)
        return result

    def synchronize_ifc(
        self,
        baseline: Any,
        aias: Any,
        ifc: Any,
        allowed_properties: set[str],
    ) -> Any:
        """Synchronize baseline, AIAS, and IFC interchange models."""
        result = self.ifc.synchronize(
            baseline,
            aias,
            ifc,
            allowed_properties,
        )
        self._ifc_runs.append(result)
        return result

    def export_ifc_entities(self, model: Any) -> Any:
        """Export neutral IFC entities from an interchange model."""
        result = self.ifc.export_entities(model)
        self._ifc_runs.append(result)
        return result

    def import_ifc_entities(
        self,
        model_id: str,
        version: str,
        entities: tuple[Any, ...],
        source: str,
    ) -> Any:
        """Import neutral IFC entities into a native interchange model."""
        result = self.ifc.import_entities(
            model_id,
            version,
            entities,
            source,
        )
        self._ifc_runs.append(result)
        return result

    def create_delivery_manifest(
        self,
        source: str | Path,
        *,
        package_id: str,
        revision: str,
        source_package: str,
    ) -> Any:
        """Create a native revision manifest for a delivery source package."""
        manifest = create_revision_manifest(
            Path(source),
            package_id,
            revision,
            source_package,
        )
        self._delivery_manifests.append(manifest)
        return manifest

    def snapshot(self) -> CoordinationSnapshot:
        """Return a compact snapshot of current coordination activity."""
        federated = self.collaboration.federated_models()
        issue_items = getattr(self.issues, "issues", None)
        if issue_items is None:
            issue_items = getattr(self.issues, "_issues", ())
        history = getattr(self.versions, "history", {})

        return CoordinationSnapshot(
            federated_models=len(federated),
            issues=len(issue_items),
            revisioned_objects=len(history),
            clash_runs=len(self._clash_runs),
            validation_runs=len(self._validation_runs),
            quality_runs=len(self._quality_runs),
            boq_runs=len(self._boq_runs),
            ifc_runs=len(self._ifc_runs),
            delivery_manifests=len(self._delivery_manifests),
        )
