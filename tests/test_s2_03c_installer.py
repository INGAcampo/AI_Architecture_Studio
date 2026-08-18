from pathlib import Path
def test_modules_exist():
    r=Path(__file__).resolve().parents[1]
    for p in ('src/gui/inspector/controller.py','src/gui/inspector/panel.py','src/gui/inspector/editor_factory.py','scripts/install_s2_03c.py'):assert (r/p).exists()
