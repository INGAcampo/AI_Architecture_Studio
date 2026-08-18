from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_continuity_installer_preserves_python_package_layout():
 installer=ROOT/"AIAS_GOV_CONTINUITY001_VERIFIABLE_HANDOFF_INSTALLER";payload=installer/"payload/src"
 assert (payload/"aias_context_engine/__init__.py").is_file()
 assert (payload/"aias_context_engine/builder.py").is_file()
 assert not any((payload/name).exists() for name in ("builder.py","cli.py","continuity.py","storage.py"))
 source=(installer/"install_gov_continuity001.py").read_text(encoding="utf-8")
 assert 'r/"src/aias_context_engine"' in source
 assert 'env["PYTHONPATH"]' in source
