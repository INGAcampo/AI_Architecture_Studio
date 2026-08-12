from dataclasses import dataclass
from .candidate import DesignCandidate

@dataclass(frozen=True, slots=True)
class PopulationSnapshot:
    generation: int
    size: int
    candidate_ids: tuple[str, ...]

class PopulationManager:
    def __init__(self):
        self._candidates: dict[str, DesignCandidate] = {}
        self.generation = 0

    def add(self, candidate: DesignCandidate):
        self._candidates[candidate.candidate_id] = candidate

    def remove(self, candidate_id: str):
        return self._candidates.pop(candidate_id)

    def all(self):
        return tuple(self._candidates.values())

    def clear(self):
        self._candidates.clear()

    def advance_generation(self):
        self.generation += 1
        return self.generation

    def snapshot(self):
        return PopulationSnapshot(
            generation=self.generation,
            size=len(self._candidates),
            candidate_ids=tuple(sorted(self._candidates)),
        )
