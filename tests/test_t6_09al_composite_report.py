import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.composites.progressive_damage_loop import ProgressiveDamageLoop
    from analysis.composites.composite_report import CompositeReportEngine
    assert 'Progressive Composite Damage' in CompositeReportEngine().build(ProgressiveDamageLoop().run(.8),.3).markdown
