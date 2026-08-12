import pytest
from engines.civil.pavement import *

@pytest.mark.parametrize("index", range(120))
def test_pavement(index):
    section = PavementSection(
        f"S{index}",
        (
            PavementLayer("AC", 0.10, 3000, 0.44),
            PavementLayer("BASE", 0.20, 300, 0.14),
        ),
    )
    engine = PavementDesignEngine()
    assert engine.total_thickness(section) == pytest.approx(0.30)
    assert engine.structural_number(section) > 0
