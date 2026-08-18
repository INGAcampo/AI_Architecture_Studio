class DummyColumn:

    volume = 1.0
    density_kg_m3 = 2400.0
    supported_slab_load_kg = 1000.0
    supported_beam_load_kg = 500.0
    supported_live_load_kg = 300.0


def test_placeholder():

    from engines.structural.column_analysis import ColumnAnalysis

    c = DummyColumn()

    assert ColumnAnalysis.service_load(c) == 4200.0
