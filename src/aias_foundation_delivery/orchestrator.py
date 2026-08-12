"""Transmittal construction, source preservation and checksum release orchestration."""
from __future__ import annotations

import csv
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

from aias_foundation_documentation.orchestrator import FoundationDocumentationOrchestrator

from .engine import FoundationDeliveryEngine
from .models import ApprovalEvidence, CoordinationIssue


class FoundationDeliveryOrchestrator:
    """Coordinate a complete revision and package independently verifiable evidence."""
    VERSION = "1.0.0"

    def execute(self, workspace: Path, source: Path | None = None, revision: str = "R00", approval: ApprovalEvidence | None = None, issues: list[CoordinationIssue] | None = None) -> dict:
        """Preserve source artifacts and produce transmittal manifests and release ZIP."""
        workspace.mkdir(parents=True, exist_ok=True)
        source = source or workspace / "source_ecp000001d"
        if not source.exists():
            FoundationDocumentationOrchestrator().execute(source)
        package = FoundationDeliveryEngine().coordinate(source, revision, approval, issues)
        delivery = workspace / "transmittal"
        if delivery.exists():
            shutil.rmtree(delivery)
        # Preserve every source artifact covered by the revision manifest so a
        # downstream consumer can independently verify the complete chain.
        shutil.copytree(source, delivery, ignore=shutil.ignore_patterns("release"))
        (delivery / "coordination").mkdir(parents=True)
        (delivery / "coordination" / "revision_manifest.json").write_text(json.dumps(package.revision_manifest.to_dict(), indent=2) + "\n", encoding="utf-8")
        (delivery / "coordination" / "issue_register.json").write_text(json.dumps([issue.to_dict() for issue in package.issues], indent=2) + "\n", encoding="utf-8")
        with (delivery / "coordination" / "issue_register.csv").open("w", encoding="utf-8", newline="") as stream:
            writer = csv.writer(stream); writer.writerow(["issue_id", "title", "description", "owner", "status", "resolution"])
            for issue in package.issues: writer.writerow([issue.issue_id, issue.title, issue.description, issue.owner, issue.status.value, issue.resolution or ""])
        manifest_path = delivery / "TRANSMITTAL_MANIFEST.json"
        manifest_path.write_text(json.dumps(package.to_dict(), indent=2) + "\n", encoding="utf-8")
        release = workspace / "release"; release.mkdir(exist_ok=True)
        archive = release / f"ECP-000001E_FOUNDATION_COORDINATION_DELIVERY_{self.VERSION}_{revision}.zip"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as bundle:
            for path in sorted(delivery.rglob("*")):
                if path.is_file(): bundle.write(path, path.relative_to(delivery))
        checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
        (release / f"{archive.name}.sha256").write_text(f"{checksum}  {archive.name}\n", encoding="utf-8")
        return {"validated": True, "package_id": package.package_id, "revision": revision, "source_package": package.source_package, "delivery_status": package.delivery_status, "complete": package.completeness["complete"], "file_count": len(package.revision_manifest.files), "open_issues": sum(i.status.value == "OPEN" for i in package.issues), "archive": str(archive), "sha256": checksum}
