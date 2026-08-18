"""Public module supporting autonomous engineering planning and controlled execution."""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

@dataclass(slots=True)
class AssetRecord:
    """Execute the public AssetRecord operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
    asset_id: str
    asset_type: str
    domain: str
    version: str
    payload: dict[str, Any]
    reusable: bool = True

@dataclass(slots=True)
class PipelinePlan:
    """Execute the public PipelinePlan operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
    plan_id: str
    stages: list[str]
    parallel_groups: list[list[str]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(slots=True)
class BuildResult:
    """Execute the public BuildResult operation for autonomous engineering planning and controlled execution using explicit caller inputs."""
    certified: bool
    cache_hit: bool
    artifacts: list[Path]
    reports: dict[str, Any]
