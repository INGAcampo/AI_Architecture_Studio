import pytest
from engines.civil.cross_sections import *

@pytest.mark.parametrize("index", range(120))
def test_cross_sections(index):
    template = RoadTemplate(
        f"T{index}",
        (
            CrossSectionComponent("L1", 3.5, -0.02, "asphalt"),
            CrossSectionComponent("L2", 3.5, -0.02, "asphalt"),
            CrossSectionComponent("S1", 1.5, -0.04, "shoulder"),
        ),
    )
    engine = CrossSectionEngine()
    assert engine.total_width(template) == pytest.approx(8.5)
    assert engine.material_widths(template)["asphalt"] == 7.0
