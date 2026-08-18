"""Comprobador estático de integridad de imports internos de AIAS.

Uso:
    python scripts/check_import_integrity.py

No importa módulos ni ejecuta la aplicación. Analiza el AST y comprueba
que los módulos internos absolutos tengan un archivo o paquete válido.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
INTERNAL_ROOTS = {"commands", "core", "engines", "gui", "models", "config"}


@dataclass(frozen=True)
class MissingImport:
    source: Path
    line: int
    module: str


def module_exists(module: str) -> bool:
    parts = module.split(".")
    file_candidate = SRC.joinpath(*parts).with_suffix(".py")
    package_candidate = SRC.joinpath(*parts, "__init__.py")
    return file_candidate.exists() or package_candidate.exists()


def scan_file(path: Path) -> list[MissingImport]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, UnicodeDecodeError):
        return []

    missing: list[MissingImport] = []
    for node in ast.walk(tree):
        module = None
        if isinstance(node, ast.ImportFrom):
            if node.level == 0:
                module = node.module
        elif isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".", 1)[0]
                if root in INTERNAL_ROOTS and not module_exists(alias.name):
                    missing.append(
                        MissingImport(path, node.lineno, alias.name)
                    )
            continue

        if not module:
            continue
        root = module.split(".", 1)[0]
        if root in INTERNAL_ROOTS and not module_exists(module):
            missing.append(MissingImport(path, node.lineno, module))
    return missing


def main() -> int:
    if not SRC.exists():
        print(f"ERROR: no existe {SRC}")
        return 2

    missing: list[MissingImport] = []
    for path in sorted(SRC.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        missing.extend(scan_file(path))

    print("AIAS — COMPROBACIÓN DE INTEGRIDAD DE IMPORTS")
    print("=" * 58)
    print(f"Raíz: {ROOT}")
    print(f"Archivos Python revisados: {sum(1 for _ in SRC.rglob('*.py'))}")

    if missing:
        print(f"\nImports internos no resueltos: {len(missing)}")
        for item in missing:
            relative = item.source.relative_to(ROOT)
            print(f"- {relative}:{item.line} -> {item.module}")
        return 1

    print("\nRESULTADO: IMPORTS INTERNOS CORRECTOS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
