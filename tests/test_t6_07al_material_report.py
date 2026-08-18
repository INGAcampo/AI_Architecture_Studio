import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.materials.material_state import MaterialState
    from analysis.materials.material_report import MaterialReportEngine
    s=MaterialState((1,)*6,(0,)*6,0,0,False);assert 'Advanced Material Plasticity' in MaterialReportEngine().build(s,'J2').markdown
