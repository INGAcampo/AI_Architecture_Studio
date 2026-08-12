import pytest
from engines.structural.energy_analysis import *

@pytest.mark.parametrize("index", range(120))
def test_energy_analysis(index):
    engine = EnergyAnalysisFoundation()
    use = EnergyUse(
        f"U{index}",
        list(EnergyCarrier)[index % len(EnergyCarrier)],
        1000 + index,
        100 + index,
    )
    assert use.intensity > 0
    assert engine.total_energy((use,)) == 1000 + index
    assert engine.energy_use_intensity((use,)) == pytest.approx(use.intensity)
