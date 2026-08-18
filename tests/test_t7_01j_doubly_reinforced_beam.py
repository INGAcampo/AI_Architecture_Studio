import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.doubly_reinforced_beam import DoublyReinforcedBeamDesigner
    assert DoublyReinforcedBeamDesigner().compression_steel(200,100,1,10)==10
