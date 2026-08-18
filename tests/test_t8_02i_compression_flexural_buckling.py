import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.compression_flexural_buckling import FlexuralBucklingEngine
    assert FlexuralBucklingEngine().nominal_strength_n(200,5000)==1000000
