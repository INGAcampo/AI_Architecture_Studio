import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.beam_flexure_minor import MinorAxisFlexureEngine
    assert MinorAxisFlexureEngine().nominal_moment_nmm(345,2e5)==69e6
