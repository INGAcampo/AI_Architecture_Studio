from __future__ import annotations
import ast
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

def test_s0_02_scripts_are_valid_python():
    scripts = [
        PROJECT_ROOT / 'scripts' / 'aias_import_audit.py',
        PROJECT_ROOT / 'scripts' / 'aias_repo_inventory.py',
    ]
    for path in scripts:
        assert path.is_file()
        ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))

def test_conftest_registers_src_as_import_root():
    source = (PROJECT_ROOT / 'tests' / 'conftest.py').read_text(encoding='utf-8-sig')
    assert 'PROJECT_ROOT / "src"' in source
    assert 'sys.path.insert(0, src_path)' in source
