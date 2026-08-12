"""Public module supporting advanced AEPS production, governance and observability."""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

@dataclass(slots=True)
class DomainTemplate:
    """Execute the public DomainTemplate operation for advanced AEPS production, governance and observability using explicit caller inputs."""
    template_id: str
    name: str
    domain: str
    files: dict[str, str]
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(slots=True)
class GeneratedModule:
    """Execute the public GeneratedModule operation for advanced AEPS production, governance and observability using explicit caller inputs."""
    module_name: str
    root: Path
    artifacts: list[Path] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(slots=True)
class CertificationBundle:
    """Execute the public CertificationBundle operation for advanced AEPS production, governance and observability using explicit caller inputs."""
    certified: bool
    issues: list[str]
    reports: dict[str, Any]
    output_dir: Path
