from __future__ import annotations
import ast
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

EXCLUDED_DIRS = {'.git','.venv','venv','__pycache__','.pytest_cache','backup','backups','dist','build'}

def included(path: Path) -> bool:
    return not any(part.lower() in EXCLUDED_DIRS for part in path.parts)

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    project_root = Path(__file__).resolve().parents[1]
    roots = [project_root / 'src', project_root / 'tests']
    python_files = sorted(path for root in roots if root.exists() for path in root.rglob('*.py') if included(path))
    syntax_errors = []
    empty_files = []
    loc = 0
    duplicate_map = defaultdict(list)
    imports = Counter()
    for path in python_files:
        relative = str(path.relative_to(project_root))
        duplicate_map[digest(path)].append(relative)
        text = path.read_text(encoding='utf-8-sig')
        loc += len(text.splitlines())
        if not text.strip():
            empty_files.append(relative)
        try:
            tree = ast.parse(text, filename=relative)
        except SyntaxError as exc:
            syntax_errors.append({'path': relative, 'line': exc.lineno, 'message': exc.msg})
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split('.')[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.update([node.module.split('.')[0]])
    duplicates = [paths for paths in duplicate_map.values() if len(paths) > 1]
    report = {
        'project_root': str(project_root),
        'python_files': len(python_files),
        'lines_of_code': loc,
        'empty_python_files': empty_files,
        'syntax_errors': syntax_errors,
        'duplicate_groups': duplicates,
        'top_import_roots': imports.most_common(30),
    }
    output_dir = project_root / 'reports'
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / 'aias_repository_inventory.json'
    output_file.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')
    print('=' * 72)
    print('AIAS REPOSITORY INVENTORY — SPRINT S0.02')
    print('=' * 72)
    print(f"Archivos Python      : {report['python_files']}")
    print(f"Líneas Python        : {report['lines_of_code']}")
    print(f"Archivos vacíos      : {len(empty_files)}")
    print(f"Errores de sintaxis  : {len(syntax_errors)}")
    print(f"Grupos duplicados    : {len(duplicates)}")
    print(f'Reporte generado     : {output_file}')
    if syntax_errors:
        print('\nESTADO: ERROR DE SINTAXIS')
        return 1
    print('\nESTADO: INVENTARIO COMPLETADO')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
