"""Public module supporting the AIAS continuity and context system."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class ComponentRecord:
    """Execute the public ComponentRecord operation for the AIAS continuity and context system using explicit caller inputs."""
    component_id: str
    name: str
    path: str
    status: str
    category: str


@dataclass(frozen=True)
class ContextManifest:
    """Execute the public ContextManifest operation for the AIAS continuity and context system using explicit caller inputs."""
    schema_version: str
    engine_version: str
    generated_at: str
    project_root: str
    identity: dict[str, Any]
    constitution: dict[str, Any]
    current_state: dict[str, Any]
    roadmap: dict[str, Any]
    components: list[ComponentRecord] = field(default_factory=list)
    installed_packages: list[str] = field(default_factory=list)
    programs_in_progress: list[dict[str, Any]] = field(default_factory=list)
    permanent_rules: list[str] = field(default_factory=list)
    aias_university: dict[str, Any] = field(default_factory=dict)
    decisions: list[dict[str, Any]] = field(default_factory=list)
    knowledge_graph: dict[str, Any] = field(default_factory=dict)
    engineering_object_index: dict[str, Any] = field(default_factory=dict)
    capabilities: list[str] = field(default_factory=list)
    sprint_history: list[dict[str, Any]] = field(default_factory=list)
    changelog: list[dict[str, Any]] = field(default_factory=list)
    artifacts: list[dict[str, Any]] = field(default_factory=list)
    integrity: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Project the current value into the stable dict representation."""
        return asdict(self)
