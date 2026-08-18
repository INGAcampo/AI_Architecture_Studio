"""Public API for AIAS production BIM interoperability and transaction support."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from pathlib import Path
import shutil
from typing import Iterable


class OfflineExchangeTarget(str, Enum):
    """Represent OfflineExchangeTarget within the AIAS production BIM interoperability layer."""
    SKETCHUP = "SKETCHUP"
    GEO5 = "GEO5"


@dataclass(frozen=True)
class ExchangeArtifact:
    """Represent ExchangeArtifact within the AIAS production BIM interoperability layer."""
    source_path: str
    staged_name: str
    extension: str
    size_bytes: int
    sha256: str

    def as_dict(self) -> dict:
        """Execute the as dict operation for this interoperability component."""
        return {
            "source_path": self.source_path,
            "staged_name": self.staged_name,
            "extension": self.extension,
            "size_bytes": self.size_bytes,
            "sha256": self.sha256,
        }


@dataclass(frozen=True)
class ExchangeBundle:
    """Represent ExchangeBundle within the AIAS production BIM interoperability layer."""
    target: OfflineExchangeTarget
    bundle_dir: str
    manifest_path: str
    artifacts: tuple[ExchangeArtifact, ...]
    vendor_runtime_verified: bool
    proprietary_format_written: bool
    launch_performed: bool

    @property
    def artifact_count(self) -> int:
        """Execute the artifact count operation for this interoperability component."""
        return len(self.artifacts)

    def as_dict(self) -> dict:
        """Execute the as dict operation for this interoperability component."""
        return {
            "target": self.target.value,
            "bundle_dir": self.bundle_dir,
            "manifest_path": self.manifest_path,
            "artifact_count": self.artifact_count,
            "artifacts": [a.as_dict() for a in self.artifacts],
            "vendor_runtime_verified": self.vendor_runtime_verified,
            "proprietary_format_written": self.proprietary_format_written,
            "launch_performed": self.launch_performed,
        }


class SafeOfflineExchangeBackend:
    """Stage neutral AIAS exchange artifacts without invoking vendor software.

    This backend deliberately does not create or claim to create proprietary vendor
    files. It copies already-existing neutral exchange artifacts into an auditable
    bundle and writes a JSON manifest containing SHA-256 hashes.

    Vendor compatibility of a neutral format is not implied by this class and must
    be verified independently against the user's installed vendor version.
    """

    allowed_extensions: frozenset[str] = frozenset()
    forbidden_proprietary_extensions: frozenset[str] = frozenset()
    target: OfflineExchangeTarget

    def __init__(self, target: OfflineExchangeTarget):
        self.target = target

    @staticmethod
    def _sha256(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def validate_source(self, source: str | Path) -> Path:
        """Execute the validate source operation for this interoperability component."""
        path = Path(source).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(path)
        if not path.is_file():
            raise ValueError(f"Exchange source is not a file: {path}")

        ext = path.suffix.lower()
        if ext in self.forbidden_proprietary_extensions:
            raise ValueError(
                f"Proprietary target format is not supported by the safe offline backend: {ext}"
            )
        if ext not in self.allowed_extensions:
            raise ValueError(
                f"Unsupported neutral exchange extension for {self.target.value}: {ext}"
            )
        return path

    def stage_bundle(
        self,
        sources: Iterable[str | Path],
        output_dir: str | Path,
        *,
        overwrite: bool = False,
    ) -> ExchangeBundle:
        """Execute the stage bundle operation for this interoperability component."""
        srcs = [self.validate_source(p) for p in sources]
        if not srcs:
            raise ValueError("At least one exchange source is required.")

        names = [p.name.lower() for p in srcs]
        if len(set(names)) != len(names):
            raise ValueError("Duplicate staged file names are not allowed.")

        bundle_dir = Path(output_dir).expanduser().resolve()
        bundle_dir.mkdir(parents=True, exist_ok=True)

        manifest_path = bundle_dir / "AIAS_EXCHANGE_MANIFEST.json"
        if manifest_path.exists() and not overwrite:
            raise FileExistsError(
                f"Exchange manifest already exists; set overwrite=True to replace it: {manifest_path}"
            )

        artifacts: list[ExchangeArtifact] = []
        copied_paths: list[Path] = []

        try:
            for src in sorted(srcs, key=lambda p: p.name.lower()):
                dst = bundle_dir / src.name
                if dst.exists() and not overwrite:
                    raise FileExistsError(
                        f"Staged artifact already exists; set overwrite=True to replace it: {dst}"
                    )

                shutil.copy2(src, dst)
                copied_paths.append(dst)

                if self._sha256(src) != self._sha256(dst):
                    raise RuntimeError(f"SHA-256 mismatch after staging: {src}")

                artifacts.append(
                    ExchangeArtifact(
                        source_path=str(src),
                        staged_name=dst.name,
                        extension=dst.suffix.lower(),
                        size_bytes=dst.stat().st_size,
                        sha256=self._sha256(dst),
                    )
                )

            payload = {
                "schema": "aias.offline-exchange.v1",
                "target": self.target.value,
                "mode": "SAFE_OFFLINE_STAGING",
                "vendor_runtime_verified": False,
                "proprietary_format_written": False,
                "launch_performed": False,
                "compatibility_certified": False,
                "compatibility_note": (
                    "This bundle contains neutral exchange artifacts only. "
                    "Vendor-version import compatibility is not certified by AIAS."
                ),
                "artifact_count": len(artifacts),
                "artifacts": [a.as_dict() for a in artifacts],
            }

            manifest_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )

            return ExchangeBundle(
                target=self.target,
                bundle_dir=str(bundle_dir),
                manifest_path=str(manifest_path),
                artifacts=tuple(artifacts),
                vendor_runtime_verified=False,
                proprietary_format_written=False,
                launch_performed=False,
            )
        except Exception:
            for dst in copied_paths:
                try:
                    dst.unlink()
                except Exception:
                    pass
            try:
                if manifest_path.exists():
                    manifest_path.unlink()
            except Exception:
                pass
            raise

    def verify_bundle(self, bundle_dir: str | Path) -> bool:
        """Execute the verify bundle operation for this interoperability component."""
        root = Path(bundle_dir).expanduser().resolve()
        manifest_path = root / "AIAS_EXCHANGE_MANIFEST.json"
        if not manifest_path.exists():
            return False

        try:
            payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            return False

        if payload.get("schema") != "aias.offline-exchange.v1":
            return False
        if payload.get("target") != self.target.value:
            return False
        if payload.get("vendor_runtime_verified") is not False:
            return False
        if payload.get("proprietary_format_written") is not False:
            return False
        if payload.get("launch_performed") is not False:
            return False

        artifacts = payload.get("artifacts")
        if not isinstance(artifacts, list) or not artifacts:
            return False
        if payload.get("artifact_count") != len(artifacts):
            return False

        names = set()
        for item in artifacts:
            name = item.get("staged_name")
            if not name or name.lower() in names:
                return False
            names.add(name.lower())

            p = root / name
            if not p.exists() or not p.is_file():
                return False
            if p.suffix.lower() not in self.allowed_extensions:
                return False
            if p.suffix.lower() in self.forbidden_proprietary_extensions:
                return False
            if p.stat().st_size != item.get("size_bytes"):
                return False
            if self._sha256(p) != item.get("sha256"):
                return False

        return True


class SketchUpOfflineExchangeBackend(SafeOfflineExchangeBackend):
    """Safe staging backend for neutral files intended for a future SketchUp workflow.

    This does not write .skp and does not claim compatibility with any SketchUp version.
    """

    allowed_extensions = frozenset({".ifc", ".dwg", ".dxf", ".dae", ".obj", ".stl"})
    forbidden_proprietary_extensions = frozenset({".skp"})
    target = OfflineExchangeTarget.SKETCHUP

    def __init__(self):
        super().__init__(OfflineExchangeTarget.SKETCHUP)


class Geo5OfflineExchangeBackend(SafeOfflineExchangeBackend):
    """Safe staging backend for neutral files intended for a future GEO5 workflow.

    This does not write GEO5-native project formats and does not claim vendor compatibility.
    """

    allowed_extensions = frozenset({".dxf", ".dwg", ".ifc", ".csv", ".txt", ".xml"})
    forbidden_proprietary_extensions = frozenset({
        ".gmk", ".gpa", ".gsp", ".gcd", ".gpf", ".gbr"
    })
    target = OfflineExchangeTarget.GEO5

    def __init__(self):
        super().__init__(OfflineExchangeTarget.GEO5)
