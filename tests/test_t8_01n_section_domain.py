import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.steel_library.section_domain import SteelSection
    s=SteelSection('X','W',1000,10,1e6,2.5e5)
    assert s.rx_mm>0
