import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.singly_reinforced_beam import SinglyReinforcedBeamDesigner
    assert SinglyReinforcedBeamDesigner().required_steel(100e6,300,500,28,420)>0
