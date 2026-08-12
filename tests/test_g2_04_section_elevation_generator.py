import pytest
from documentation_kernel.section_elevation import *

@pytest.mark.parametrize("i", range(120))
def test_views(i):
    elements = (
        ModelElement("A", 0, 0, 0, 2, 3),
        ModelElement("B", 5, 0, 0, 2, 4),
    )
    engine = SectionElevationGenerator()
    section = engine.section(f"S{i}", elements, 0, 2.5)
    elevation = engine.elevation(f"E{i}", elements)
    assert section.visible_element_ids == ("A",)
    assert elevation.visible_element_ids == ("A", "B")
    assert elevation.bounds[3] == 4
