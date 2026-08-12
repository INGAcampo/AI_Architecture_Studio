"""Read-only health check for the AI Architecture Studio repository."""

from __future__ import annotations

import ast
import sys
from dataclasses import dataclass
from pathlib import Path


IGNORED_PARTS = {
    ".git",
    ".venv",
    ".pytest_cache",
    "__pycache__",
    "backup",
    "backups",
    "build",
    "dist",
    "releases",
}


@dataclass(frozen=True)
class SyntaxFailure:
    path: Path
    line: int
    message: str


def is_ignored(path: Path) -> bool:
    return any(part in IGNORED_PARTS for part in path.parts)


def collect_python_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.py")
        if not is_ignored(path.relative_to(root))
    )


def validate_syntax(paths: list[Path]) -> list[SyntaxFailure]:
    failures: list[SyntaxFailure] = []
    for path in paths:
        try:
            ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        except (SyntaxError, UnicodeDecodeError) as exc:
            failures.append(
                SyntaxFailure(
                    path=path,
                    line=getattr(exc, "lineno", 0) or 0,
                    message=str(exc),
                )
            )
    return failures


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    src = root / "src"
    tests = root / "tests"
    pyproject = root / "pyproject.toml"

    print("AIAS Repository Health Check")
    print(f"Root: {root}")

    missing = [path for path in (src, tests, pyproject) if not path.exists()]
    if missing:
        for path in missing:
            print(f"[ERROR] Falta: {path.relative_to(root)}")
        return 2

    python_files = collect_python_files(root)
    failures = validate_syntax(python_files)

    print(f"[OK] Archivos Python inspeccionados: {len(python_files)}")
    print("[OK] src/, tests/ y pyproject.toml presentes")

    if failures:
        for failure in failures:
            relative = failure.path.relative_to(root)
            print(f"[ERROR] {relative}:{failure.line}: {failure.message}")
        return 1

    print("[OK] No se detectaron errores de sintaxis")
    print("ESTADO: SALUDABLE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
