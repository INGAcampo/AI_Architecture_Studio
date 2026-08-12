"""In-memory immutable snapshots supporting engineering-object revision history."""
from __future__ import annotations
from dataclasses import dataclass, field
import copy
from .models import EngineeringObject

@dataclass(slots=True)
class VersionStore:
    """Retain deep-copied object snapshots keyed by stable engineering identity."""
    history: dict[str, list[dict]] = field(default_factory=dict)

    def snapshot(self, obj: EngineeringObject, note: str) -> None:
        """Append a deep immutable snapshot of the current object revision."""
        self.history.setdefault(obj.object_id, []).append({
            "version":obj.version,
            "revision":obj.state.revision,
            "note":note,
            "data":copy.deepcopy(obj.to_dict())
        })

    def revisions(self, object_id: str) -> int:
        """Return the number of retained snapshots for an object identity."""
        return len(self.history.get(object_id, []))
