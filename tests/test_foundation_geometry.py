from models.structural.foundation import Foundation


def test_foundation_volume():

    foundation = Foundation(
        width=2.0,
        length=2.0,
        thickness=0.5,
    )

    assert foundation.volume == 2.0
