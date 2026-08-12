import pytest
from documentation_kernel.schedule_engine import *

@pytest.mark.parametrize("i", range(120))
def test_schedule(i):
    elements = (
        {"mark": "D2", "width": 1.0},
        {"mark": "D1", "width": 0.9},
    )
    columns = (ScheduleColumn("mark", "Mark"), ScheduleColumn("width", "Width"))
    engine = ScheduleEngine()
    schedule = engine.build(f"S{i}", elements, columns, sort_key=lambda e: e["mark"])
    assert schedule.rows[0][0] == "D1"
    assert engine.total(schedule, 1) == pytest.approx(1.9)
