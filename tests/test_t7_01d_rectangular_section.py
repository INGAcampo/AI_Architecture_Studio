import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.rectangular_section import RectangularSection
    assert RectangularSection(300,500,450).gross_inertia()>0
