class DummyBeam:

    volume = 0.50
    density_kg_m3 = 2400.0
    length = 6.0
    distributed_load_kg_m = 1000.0


def test_beam_analysis():

    from engines.structural.beam_analysis import BeamAnalysis

    beam = DummyBeam()

    assert BeamAnalysis.maximum_shear(beam) == 3000.0
    assert BeamAnalysis.maximum_moment(beam) == 4500.0
