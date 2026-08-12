"""Public module supporting the AIAS continuity and context system."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from .models import ComponentRecord


COMPONENT_PREFIXES = (
    "AIAS_AMP", "AIAS_ECP", "AIAS_ADF", "AIAS_AEPS", "AIAS_BIM",
    "AIAS_CAD", "AIAS_G", "AIAS_S", "AIAS_TITAN", "AIAS_OMEGA",
)


def sha256_file(path: Path) -> str:
    """Execute the public sha256_file operation for the AIAS continuity and context system using explicit caller inputs."""
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class RepositoryScanner:
    """Execute the public RepositoryScanner operation for the AIAS continuity and context system using explicit caller inputs."""
    def __init__(self, project_root: Path):
        self.root = project_root.resolve()

    def components(self) -> list[ComponentRecord]:
        """Execute the public RepositoryScanner.components operation for the AIAS continuity and context system using explicit caller inputs."""
        records: list[ComponentRecord] = []
        for path in sorted(self.root.iterdir(), key=lambda p: p.name.casefold()):
            if not path.is_dir() or not path.name.startswith(COMPONENT_PREFIXES):
                continue
            category = "installer" if "INSTALLER" in path.name else "program_pack"
            status = "installed" if category == "installer" else "available"
            records.append(ComponentRecord(path.name, self._title(path.name), path.name, status, category))
        return records

    def source_packages(self) -> list[str]:
        """Execute the public RepositoryScanner.source_packages operation for the AIAS continuity and context system using explicit caller inputs."""
        source = self.root / "src"
        if not source.exists():
            return []
        return sorted(p.name for p in source.iterdir() if p.is_dir() and not p.name.startswith((".", "__")))

    def test_inventory(self) -> dict[str, int]:
        """Execute the public RepositoryScanner.test_inventory operation for the AIAS continuity and context system using explicit caller inputs."""
        tests = self.root / "tests"
        files = list(tests.glob("test_*.py")) if tests.exists() else []
        return {"test_files": len(files), "ace_test_files": sum(p.name == "test_ace_context_engine.py" or "context_engine" in p.name for p in files)}

    def artifacts(self, limit: int = 200) -> list[dict[str, object]]:
        """Execute the public RepositoryScanner.artifacts operation for the AIAS continuity and context system using explicit caller inputs."""
        candidates: list[Path] = []
        for folder in ("releases", "output", "ACKC"):
            base = self.root / folder
            if base.exists():
                candidates.extend(p for p in base.rglob("*") if p.is_file())
        result = []
        for path in sorted(candidates, key=lambda p: str(p).casefold())[:limit]:
            result.append({"path": str(path.relative_to(self.root)), "size": path.stat().st_size})
        return result

    def constitutional_compliance(self) -> dict[str, dict[str, object]]:
        """Execute the public RepositoryScanner.constitutional_compliance operation for the AIAS continuity and context system using explicit caller inputs."""
        result: dict[str, dict[str, object]] = {}
        engineering = self.root / "engineering"
        if not engineering.exists():
            return result
        for report_path in engineering.glob("*/compliance/QUALITY_GATES.json"):
            try:
                report = json.loads(report_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            component_id = report.get("component_id")
            if component_id:
                result[component_id] = {
                    "all_passed": bool(report.get("all_passed")),
                    "gates": {gate["gate_id"]: bool(gate["passed"]) for gate in report.get("gates", [])},
                    "evidence": str(report_path.relative_to(self.root)),
                }
        return dict(sorted(result.items()))

    @staticmethod
    def _title(value: str) -> str:
        return value.replace("_", " ").replace("INSTALLER", "").strip()
