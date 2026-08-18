import pytest
from ai_kernel.generative_layout import *

@pytest.mark.parametrize("i", range(120))
def test_layout(i):
    requirements = (
        SpaceRequirement("living", 20, 1.25),
        SpaceRequirement("kitchen", 12, 1.0),
    )
    engine = GenerativeLayoutEngine()
    layout = engine.generate_linear(requirements, corridor_width=1.0)
    assert len(layout.spaces) == 2
    assert layout.total_area == pytest.approx(32)
    assert layout.compactness > 0
    assert engine.adjacency_score(layout, (("living", "kitchen"),)) > 0
