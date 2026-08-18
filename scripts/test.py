r"""
AI Architecture Studio
Sprint S0.02B — ejecutor multiplataforma de pruebas.

Ejemplos:
    python .\scripts\test.py
    python .\scripts\test.py tests/test_s0_02_repository_tools.py
    python .\scripts\test.py --fast
    python .\scripts\test.py --collect-only
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def build_command(args: argparse.Namespace) -> list[str]:
    command = [sys.executable, "-m", "pytest"]

    if args.collect_only:
        command.extend(["--collect-only", "-q"])
    elif args.fast:
        command.extend(["-q", "--maxfail=1"])
    else:
        command.append("-q")

    if args.path:
        command.append(args.path)

    extra = list(args.pytest_args or [])
    if extra and extra[0] == "--":
        extra = extra[1:]
    command.extend(extra)

    return command


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Ejecutor oficial multiplataforma de pruebas de AIAS."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default="",
        help="Archivo o carpeta de pruebas opcional.",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Detiene la ejecución después del primer fallo.",
    )
    parser.add_argument(
        "--collect-only",
        action="store_true",
        help="Muestra las pruebas que Pytest recopilaría sin ejecutarlas.",
    )
    parser.add_argument(
        "pytest_args",
        nargs=argparse.REMAINDER,
        help="Argumentos adicionales para Pytest después de --.",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    if not (project_root / "tests").is_dir():
        print(f"ERROR: no se encontró la carpeta tests en {project_root}")
        return 2

    command = build_command(args)

    print()
    print("AIAS — EJECUTOR OFICIAL DE PRUEBAS")
    print("=" * 72)
    print(f"Raíz   : {project_root}")
    print(f"Python : {sys.executable}")
    print(f"Comando: {' '.join(command)}")
    print()

    completed = subprocess.run(command, cwd=project_root, check=False)

    print()
    if completed.returncode == 0:
        print("RESULTADO: PRUEBAS CORRECTAS")
    else:
        print("RESULTADO: SE DETECTARON ERRORES")

    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
