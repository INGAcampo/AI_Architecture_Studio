"""Public module supporting AEPS repeatable generation and delivery automation."""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
@dataclass(slots=True)
class CompiledSpecification:
    """Execute the public CompiledSpecification operation for AEPS repeatable generation and delivery automation using explicit caller inputs."""
    specification_id:str; title:str; module_name:str; version:str
    requirements:list[dict[str,Any]]; dependencies:list[str]; architecture_refs:list[str]; adr_refs:list[str]
@dataclass(slots=True)
class BuildArtifact:
    """Execute the public BuildArtifact operation for AEPS repeatable generation and delivery automation using explicit caller inputs."""
    artifact_type:str; path:Path; source_id:str; checksum:str=""
@dataclass(slots=True)
class PipelineContext:
    """Execute the public PipelineContext operation for AEPS repeatable generation and delivery automation using explicit caller inputs."""
    specification:CompiledSpecification; workspace:Path
    artifacts:list[BuildArtifact]=field(default_factory=list)
    reports:dict[str,Any]=field(default_factory=dict)
