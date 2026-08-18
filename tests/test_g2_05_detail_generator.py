import pytest
from documentation_kernel.detail_generator import *

@pytest.mark.parametrize("i", range(120))
def test_detail(i):
    rules = (
        DetailRule("wall", "wall", "wall-section"),
        DetailRule("roof", "roof", "roof-edge"),
    )
    element = {"element_id": f"W{i}", "kind": "wall", "notes": ("Impermeabilizar",)}
    detail = DetailGenerator().generate(f"DET{i}", element, rules, scale=5)
    assert detail.template == "wall-section"
    assert detail.scale == 5
    assert detail.notes == ("Impermeabilizar",)
