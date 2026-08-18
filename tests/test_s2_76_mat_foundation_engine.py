import pytest
from engines.geotechnical.mat_foundations import *
@pytest.mark.parametrize("i",range(120))
def test_mat(i):
    m=MatFoundation(f"M{i}",10,8,.8,(ColumnLoad("C1",2,2,1000+i),ColumnLoad("C2",8,6,1000+i)),20000)
    e=MatFoundationEngine()
    assert e.total_load(m)==pytest.approx(2000+2*i) and e.concrete_volume(m)==64
