class DummyFoundation:

    volume = 2.0
    density_kg_m3 = 2400.0

    area = 4.0

    supported_column_load_kg = 5000.0

    soil_bearing_capacity_kpa = 5000.0


def test_foundation_analysis():

    from engines.structural.foundation_analysis import (
        FoundationAnalysis
    )

    foundation = DummyFoundation()

    assert (
        FoundationAnalysis.soil_pressure(
            foundation
        ) == 2450.0
    )
