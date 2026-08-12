import pytest
from documentation_kernel.layout_viewports import *

@pytest.mark.parametrize("i", range(120))
def test_layout(i):
    manager = LayoutViewportManager()
    item = LayoutItem(f"I{i}", 0, 0, 200, 100)
    assert manager.fit(item, 420, 297, margin=10) > 1
    arranged = manager.arrange_grid((item, item, item), 2, gap=5)
    assert arranged[1].x == 205
    assert arranged[2].y == 105
