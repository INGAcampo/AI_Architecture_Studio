import pytest
from documentation_kernel.intelligent_tags import *

@pytest.mark.parametrize("i", range(120))
def test_tags(i):
    engine = IntelligentTagEngine()
    template = TagTemplate("door-tag", "{mark} | {width}x{height}")
    result = engine.render(f"D{i}", {"mark": f"P-{i}", "width": 0.9, "height": 2.1}, template)
    assert result.text == f"P-{i} | 0.9x2.1"
    assert result.missing_fields == ()
