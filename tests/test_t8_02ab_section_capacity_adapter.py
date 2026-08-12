import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.section_capacity_adapter import SectionCapacityAdapter
    class S:
        ix_mm4=1_000_000.0
        depth_mm=200.0
    assert SectionCapacityAdapter().plastic_modulus_mm3(S())==pytest.approx(10000.0)
