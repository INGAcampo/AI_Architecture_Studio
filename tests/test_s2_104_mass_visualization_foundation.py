import pytest
from engines.civil.mass_visualization import *

@pytest.mark.parametrize("i", range(120))
def test_visualization(i):
    batches = (
        RenderBatch("A",100+i,1000),
        RenderBatch("B",50,500),
    )
    e = MassVisualizationFoundation()
    assert e.total_objects(batches) == 150+i
    assert e.total_triangles(batches) == 1500
