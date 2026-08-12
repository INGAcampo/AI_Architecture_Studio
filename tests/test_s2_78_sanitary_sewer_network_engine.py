import pytest
from engines.civil.sanitary_sewer import *

@pytest.mark.parametrize("index", range(120))
def test_sanitary_sewer(index):
    pipe = SewerPipe(
        f"S{index}", 0.25 + index*0.0005, 0.01, 0.013, 0.8
    )
    engine = SanitarySewerEngine()
    assert engine.full_flow_area(pipe) > 0
    assert engine.hydraulic_radius(pipe) > 0
    assert engine.capacity_manning(pipe) > 0
