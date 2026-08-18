"""End-to-end ECP-000001F dossier and release orchestration."""
from __future__ import annotations
import hashlib, json, zipfile
from pathlib import Path
from aias_foundation_delivery.orchestrator import FoundationDeliveryOrchestrator
from .engine import FoundationHandoverEngine

class FoundationHandoverOrchestrator:
    """Generate an upstream delivery and package its lifecycle dossier."""
    VERSION = "1.0.0"
    def execute(self, workspace: Path, transmittal: Path | None = None) -> dict:
        """Build a verifiable handover dossier and checksum-protected release archive."""
        workspace.mkdir(parents=True, exist_ok=True)
        if transmittal is None:
            source = workspace / "source_ecp000001e"; FoundationDeliveryOrchestrator().execute(source); transmittal = source / "transmittal"
        dossier = FoundationHandoverEngine().build(transmittal)
        dossier_dir = workspace / "lifecycle_dossier"; dossier_dir.mkdir(exist_ok=True)
        dossier_path = dossier_dir / "FOUNDATION_HANDOVER_DOSSIER.json"; dossier_path.write_text(json.dumps(dossier, indent=2)+"\n", encoding="utf-8")
        (dossier_dir / "FINDINGS.json").write_text(json.dumps(dossier["findings"], indent=2)+"\n", encoding="utf-8")
        (dossier_dir / "CUSTODY_LEDGER.json").write_text(json.dumps(dossier["custody"], indent=2)+"\n", encoding="utf-8")
        release = workspace / "release"; release.mkdir(exist_ok=True)
        archive = release / f"ECP-000001F_FOUNDATION_DIGITAL_HANDOVER_{self.VERSION}.zip"
        with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as bundle:
            for path in sorted(dossier_dir.rglob("*")):
                if path.is_file(): bundle.write(path,path.relative_to(dossier_dir))
        checksum=hashlib.sha256(archive.read_bytes()).hexdigest(); (release/f"{archive.name}.sha256").write_text(f"{checksum}  {archive.name}\n",encoding="utf-8")
        return {"validated":True,"handover_id":dossier["handover_id"],"maturity_level":dossier["maturity"]["level"],"level_5_evidence_complete":dossier["maturity"]["level_5_achieved"],"kpi_time_reduction":dossier["kpi"]["time_reduction"],"kpi_classification":dossier["kpi"]["classification"],"archive":str(archive),"sha256":checksum}
