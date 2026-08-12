from models.structural.beam import Beam


def test_beam_length():

    beam = Beam(
        start_point=(0.0, 0.0),
        end_point=(3.0, 4.0),
    )

    assert beam.length == 5.0
