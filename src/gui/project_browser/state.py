from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ProjectBrowserState:
    expanded_node_ids: set[str] = field(default_factory=set)
    selected_node_id: str | None = None
    filter_text: str = ""

    def snapshot(self) -> dict[str, Any]:
        return {
            "expanded_node_ids": sorted(self.expanded_node_ids),
            "selected_node_id": self.selected_node_id,
            "filter_text": self.filter_text,
        }

    @classmethod
    def from_snapshot(cls, data: dict[str, Any]) -> "ProjectBrowserState":
        return cls(
            expanded_node_ids=set(
                str(item) for item in data.get("expanded_node_ids", [])
            ),
            selected_node_id=data.get("selected_node_id"),
            filter_text=str(data.get("filter_text", "")),
        )
