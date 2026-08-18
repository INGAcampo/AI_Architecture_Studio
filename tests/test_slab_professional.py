"""Pruebas básicas para SLAB 5.0.8.1."""

from models.architectural.room import Room
from models.architectural.slab import Slab
from engines.geometry.point import Point


def test_slab_volume():
    room = Room(
        boundary=[
            Point(0, 0, 0),
            Point(10, 0, 0),
            Point(10, 5, 0),
            Point(0, 5, 0),
        ],
        name="Sala",
        seed_point=Point(5, 2.5, 0),
    )
    slab = Slab(host_room=room, thickness=0.15)
    assert abs(slab.area - 50.0) < 1.0e-8
    assert abs(slab.volume - 7.5) < 1.0e-8


if __name__ == "__main__":
    test_slab_volume()
    print("SLAB PROFESSIONAL: OK")
