import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.retaining_walls.vertical_slice import VerticalSlice
    r=VerticalSlice().run()
    assert r.status=='PASS' and r.utilization<1
