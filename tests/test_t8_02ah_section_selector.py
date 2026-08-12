import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.section_selector import SectionSelector
    r=SectionSelector().lightest_passing(({'status':'PASS','mass_kg_m':50},{'status':'PASS','mass_kg_m':40}))
    assert r['mass_kg_m']==40
