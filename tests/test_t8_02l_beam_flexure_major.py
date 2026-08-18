import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.beam_flexure_major import MajorAxisFlexureEngine
    assert MajorAxisFlexureEngine().nominal_moment_nmm(345,1e6)==345e6
