from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ConstructionTask:
    task_id: str
    start_day: int
    duration_days: int

    @property
    def end_day(self):
        return self.start_day+self.duration_days

class Infrastructure4DSequencer:
    def project_duration(self, tasks):
        return max(t.end_day for t in tasks)-min(t.start_day for t in tasks)

    def overlaps(self, a, b):
        return a.start_day < b.end_day and b.start_day < a.end_day
