import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.shells.laminate_resultants import LaminateResultantsEngine
    I=((1,0,0),(0,1,0),(0,0,1));Z=((0,0,0),(0,0,0),(0,0,0));n,m=LaminateResultantsEngine().calculate(I,Z,I,(1,2,3),(4,5,6));assert n==(1,2,3) and m==(4,5,6)
