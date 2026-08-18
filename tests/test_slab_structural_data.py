"""Pruebas SLAB 5.0.8.4."""

from engines.geometry.point import Point
from models.architectural.room import Room
from models.architectural.slab import Slab


def test_structural_loads():
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

    slab = Slab(
        host_room=room,
        thickness=0.20,
        density_kg_m3=2400.0,
        superimposed_dead_load_kg_m2=100.0,
        finish_load_kg_m2=50.0,
        live_load_kg_m2=200.0,
    )

    assert abs(slab.area - 50.0) < 1.0e-8
    assert abs(slab.volume - 10.0) < 1.0e-8
    assert abs(slab.self_weight_kg_m2 - 480.0) < 1.0e-8
    assert abs(slab.total_dead_load_kg_m2 - 630.0) < 1.0e-8
    assert abs(slab.total_service_load_kg_m2 - 830.0) < 1.0e-8
    assert abs(slab.total_service_load_kg - 41500.0) < 1.0e-8


if __name__ == "__main__":
    test_structural_loads()
    print("SLAB STRUCTURAL DATA: OK")
