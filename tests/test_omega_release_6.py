import pytest
from aias_omega_release6.workflow import build_and_export

@pytest.mark.parametrize("i", range(200))
def test_boq_export(tmp_path,i):
    project,lines,paths=build_and_export(tmp_path/str(i))
    assert len(lines)==2
    assert all(p.is_file() for p in paths.values())
    assert sum(x.total for x in lines)>0

@pytest.mark.parametrize("i", range(100))
def test_report_content(tmp_path,i):
    project,lines,paths=build_and_export(tmp_path/str(i))
    text=paths["md"].read_text(encoding="utf-8")
    assert "AIAS Engineering Summary" in text
    assert "CONC-WALL" in text
    assert "CONC-SLAB" in text
