import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.materials.return_mapping import RadialReturnMapping
    assert RadialReturnMapping().integrate((350,0,0,0,0,0),80000,250).yielded
