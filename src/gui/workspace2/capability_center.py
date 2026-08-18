"""Application-visible, read-only authority over AIAS platform delivery evidence."""
from __future__ import annotations

import hashlib
import html
import json
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath

from gui.workspace.model import DockArea, PanelDescriptor


@dataclass(frozen=True, slots=True)
class InstallerEvidence:
    """Summarize one installer without executing or modifying it."""

    name: str
    pack_id: str
    version: str
    status: str
    files: int
    integrity_valid: bool
    publisher_signed: bool


class CapabilityCenter:
    """Collect repository evidence for a Workspace panel and governed commands."""

    PANEL_ID = "AIAS_CAPABILITY_CENTER"

    def __init__(self, project_root: str | Path) -> None:
        self.root = Path(project_root).resolve()
        if not (self.root / "src").is_dir() or not (self.root / "engineering").is_dir():
            raise ValueError("invalid_aias_project_root")

    def panel_descriptor(self) -> PanelDescriptor:
        """Return the stable Workspace panel contract."""
        return PanelDescriptor(
            self.PANEL_ID,
            "AIAS Capability Center",
            DockArea.RIGHT,
            category="platform",
            metadata={"spec_id": "EXP-PLATFORM-GUI-001", "read_only_evidence": True},
        )

    def snapshot(self) -> dict:
        """Build a truthful product snapshot from canonical repository evidence."""
        ace = self._read_json(self.root / "ACKC/MASTER_CONTEXT.json", {})
        distribution = self._read_json(self.root / "exp_installer_iso001_outputs/OFFLINE_MEDIA_BUILD_REPORT.json", {})
        installers = tuple(self._installer_evidence(path) for path in sorted(self.root.glob("AIAS_*_INSTALLER")) if path.is_dir())
        gates = []
        for path in sorted((self.root / "engineering").glob("*/compliance/QUALITY_GATES.json")):
            report = self._read_json(path, {})
            gates.append({"component_id": report.get("component_id", path.parents[1].name), "passed": bool(report.get("all_passed", False)), "gate_count": len(report.get("gates", []))})
        valid = sum(item.integrity_valid for item in installers)
        signed = sum(item.publisher_signed for item in installers)
        repository = ace.get("current_state", {}).get("repository", {})
        return {
            "schema": "AIAS-CAPABILITY-CENTER-1.0",
            "mode": "READ_ONLY_EVIDENCE",
            "components": len(ace.get("components", [])),
            "source_packages": ace.get("current_state", {}).get("source_package_count", 0),
            "test_files": repository.get("test_files", 0),
            "installers": {"total": len(installers), "integrity_valid": valid, "integrity_invalid": len(installers) - valid, "publisher_signed": signed, "items": [asdict(item) for item in installers]},
            "quality": {"components": len(gates), "passed": sum(item["passed"] for item in gates), "items": gates},
            "distribution": {
                "offline_media_verified": bool(distribution.get("verified", False)),
                "publisher_signed": bool(distribution.get("publisher_signed", False)),
                "iso_image_created": bool(distribution.get("iso_image_created", False)),
            },
            "actions": self.available_actions(valid == len(installers) and bool(installers), bool(distribution.get("publisher_signed", False))),
        }

    @staticmethod
    def available_actions(all_integrity_valid: bool, publisher_signed: bool) -> list[dict]:
        """Expose safe plans; never execute installation or updates from the snapshot."""
        return [
            {"action_id": "REFRESH_EVIDENCE", "enabled": True, "execution": "LOCAL_READ_ONLY"},
            {"action_id": "OPEN_TEST_REPORT", "enabled": True, "execution": "LOCAL_READ_ONLY"},
            {"action_id": "PLAN_INSTALL", "enabled": all_integrity_valid and publisher_signed, "execution": "REQUIRES_EXPLICIT_CONFIRMATION", "blockers": [] if all_integrity_valid and publisher_signed else (["installer_integrity_invalid"] if not all_integrity_valid else []) + (["publisher_signature_unverified"] if not publisher_signed else [])},
            {"action_id": "PLAN_UPDATE", "enabled": False, "execution": "REQUIRES_VERIFIED_CANDIDATE_AND_RECOVERY_POINT", "blockers": ["candidate_not_selected"]},
        ]

    def _installer_evidence(self, path: Path) -> InstallerEvidence:
        manifest = self._read_json(path / "manifest.json", {})
        valid, count = self._verify_checksums(path)
        return InstallerEvidence(path.name, str(manifest.get("pack_id", "UNKNOWN")), str(manifest.get("version", "UNKNOWN")), str(manifest.get("status", "UNKNOWN")), count, valid, bool(manifest.get("publisher_signed", False)))

    @staticmethod
    def _read_json(path: Path, default: dict) -> dict:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return default

    @staticmethod
    def _verify_checksums(installer: Path) -> tuple[bool, int]:
        checksum_file = installer / "checksums.sha256"
        if not checksum_file.is_file():
            return False, 0
        count = 0
        try:
            for line in checksum_file.read_text(encoding="utf-8").splitlines():
                digest, relative = line.split("  ", 1)
                relative_path = PurePosixPath(relative)
                if relative_path.is_absolute() or ".." in relative_path.parts or len(digest) != 64:
                    return False, count
                target = installer.joinpath(*relative_path.parts)
                if not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != digest.lower():
                    return False, count
                count += 1
        except (OSError, ValueError):
            return False, count
        return count > 0, count


def register_capability_center(workspace_manager, project_root: str | Path) -> CapabilityCenter:
    """Register the panel once through the canonical Workspace manager."""
    center = CapabilityCenter(project_root)
    if center.PANEL_ID not in workspace_manager.registry:
        workspace_manager.register_panel(center.panel_descriptor())
    return center


def render_capability_center(snapshot: dict) -> str:
    """Render a standalone, accessible evidence view for visual validation."""
    installers = snapshot["installers"]
    quality = snapshot["quality"]
    cards = (
        ("Componentes", snapshot["components"]),
        ("Paquetes fuente", snapshot["source_packages"]),
        ("Instaladores íntegros", f"{installers['integrity_valid']} / {installers['total']}"),
        ("Calidad conforme", f"{quality['passed']} / {quality['components']}"),
    )
    card_html = "".join(f"<article><span>{html.escape(str(label))}</span><strong>{html.escape(str(value))}</strong></article>" for label, value in cards)
    warning = "Firma editorial pendiente: instalación pública bloqueada." if not snapshot["distribution"]["publisher_signed"] else "Firma editorial verificada."
    return f"""<!doctype html><html lang='es'><meta charset='utf-8'><meta name='viewport' content='width=device-width'><title>AIAS Capability Center</title><style>:root{{--bg:#07111f;--panel:#0d1b2d;--line:#28415f;--text:#eef5ff;--muted:#9eb2c9;--cyan:#46d7ff;--amber:#ffc857}}*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:16px system-ui;padding:clamp(24px,5vw,72px)}}main{{max-width:1100px;margin:auto}}p{{color:var(--muted);max-width:70ch}}.eyebrow{{color:var(--cyan);letter-spacing:.16em;font-size:.75rem}}h1{{font-size:clamp(2.2rem,6vw,5rem);margin:.2em 0}}section{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:16px;margin:36px 0}}article{{background:var(--panel);border:1px solid var(--line);padding:24px;min-height:140px;display:flex;flex-direction:column;justify-content:space-between}}article span{{color:var(--muted)}}article strong{{font-size:2rem}}aside{{border-left:3px solid var(--amber);padding:16px 20px;background:#171b22}}code{{color:var(--cyan)}}</style><main><p class='eyebrow'>EXP-PLATFORM-GUI-001 · EVIDENCIA LOCAL</p><h1>Capability Center</h1><p>Una vista profesional de capacidades, calidad, distribución y confianza derivada del repositorio. Esta superficie no instala ni publica por sí sola.</p><section>{card_html}</section><aside role='status'><strong>Estado de distribución</strong><p>{html.escape(warning)}</p></aside><p><code>{html.escape(snapshot['schema'])}</code></p></main></html>"""
