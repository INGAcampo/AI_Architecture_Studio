from __future__ import annotations
import argparse
import ast
from dataclasses import dataclass
from pathlib import Path

EXCLUDED_DIRS = {'.git','.venv','venv','__pycache__','.pytest_cache','backup','backups','dist','build'}

@dataclass(frozen=True)
class Finding:
    category: str
    path: Path
    line: int
    detail: str

def iter_python_files(src_root: Path):
    for path in src_root.rglob('*.py'):
        if any(part.lower() in EXCLUDED_DIRS for part in path.parts):
            continue
        yield path

def audit_file(path: Path):
    findings = []
    if path.name.startswith('test_'):
        findings.append(Finding('TEST_EN_SRC', path, 1, 'Archivo de prueba localizado dentro de src.'))
    try:
        source = path.read_text(encoding='utf-8-sig')
        tree = ast.parse(source, filename=str(path))
    except (OSError, UnicodeError, SyntaxError) as exc:
        findings.append(Finding('PARSE_ERROR', path, getattr(exc, 'lineno', 1) or 1, str(exc)))
        return findings
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == 'src' or alias.name.startswith('src.'):
                    findings.append(Finding('IMPORT_SRC', path, node.lineno, f'import {alias.name}'))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            if module == 'src' or module.startswith('src.'):
                findings.append(Finding('IMPORT_SRC', path, node.lineno, f'from {module} import ...'))
    return findings

def main():
    parser = argparse.ArgumentParser(description='Audita imports y estructura de src.')
    parser.add_argument('--strict', action='store_true')
    args = parser.parse_args()
    project_root = Path(__file__).resolve().parents[1]
    src_root = project_root / 'src'
    if not src_root.is_dir():
        print(f'ERROR: no existe {src_root}')
        return 2
    files = sorted(iter_python_files(src_root))
    findings = [item for path in files for item in audit_file(path)]
    print('=' * 72)
    print('AIAS IMPORT AUDIT — SPRINT S0.02')
    print('=' * 72)
    print(f'Archivos analizados : {len(files)}')
    print(f'Hallazgos           : {len(findings)}')
    for item in findings:
        print(f'[{item.category}] {item.path.relative_to(project_root)}:{item.line} — {item.detail}')
    parse_errors = sum(i.category == 'PARSE_ERROR' for i in findings)
    src_imports = sum(i.category == 'IMPORT_SRC' for i in findings)
    tests_in_src = sum(i.category == 'TEST_EN_SRC' for i in findings)
    print('\nResumen')
    print(f'  Errores de sintaxis : {parse_errors}')
    print(f'  Imports src.*       : {src_imports}')
    print(f'  Pruebas dentro src  : {tests_in_src}')
    if parse_errors:
        print('\nESTADO: ERROR DE SINTAXIS')
        return 2
    if args.strict and (src_imports or tests_in_src):
        print('\nESTADO: NORMALIZACIÓN PENDIENTE')
        return 1
    print('\nESTADO: AUDITORÍA COMPLETADA')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
