from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ScheduleColumn:
    key: str
    heading: str

@dataclass(frozen=True, slots=True)
class Schedule:
    schedule_id: str
    columns: tuple[ScheduleColumn, ...]
    rows: tuple[tuple, ...]

class ScheduleEngine:
    def build(self, schedule_id, elements, columns, *, predicate=None, sort_key=None):
        selected = [element for element in elements if predicate is None or predicate(element)]
        if sort_key is not None:
            selected.sort(key=sort_key)
        rows = tuple(
            tuple(element.get(column.key) for column in columns)
            for element in selected
        )
        return Schedule(schedule_id, tuple(columns), rows)

    def total(self, schedule, column_index):
        return sum(row[column_index] for row in schedule.rows if isinstance(row[column_index], (int, float)))
