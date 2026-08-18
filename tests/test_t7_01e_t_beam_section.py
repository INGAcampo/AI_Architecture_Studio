import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.rc.t_beam_section import TBeamSection
    assert TBeamSection(300,1000,100,600,550).flange_width==1000
