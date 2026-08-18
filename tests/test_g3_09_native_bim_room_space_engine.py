import pytest
from bim_authoring.rooms_spaces import *

@pytest.mark.parametrize("i", range(120))
def test_room_space(i):
    room = Room(
        f"R{i}",
        "Living",
        ((0,0),(5,0),(5,4),(0,4)),
        3,
        "L1",
    )
    space = Space(f"SP{i}", room.room_id, "architecture", 4)
    engine = NativeBimRoomSpaceEngine()
    q = engine.quantities(room)
    assert q.area == pytest.approx(20)
    assert q.volume == pytest.approx(60)
    assert engine.occupancy_density(room, space) == pytest.approx(0.2)
