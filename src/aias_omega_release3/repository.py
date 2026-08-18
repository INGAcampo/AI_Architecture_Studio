"""Public module supporting the third Omega integrated product release."""
from __future__ import annotations
from pathlib import Path
from aias_omega_core.project import EngineeringProject
from .database import ProjectDatabase

class ProjectRepository:
    """Execute the public ProjectRepository operation for the third Omega integrated product release using explicit caller inputs."""
    def save(self, project: EngineeringProject, path: Path) -> Path:
        """Persist save for the third Omega integrated product release in its stable external representation."""
        db = ProjectDatabase(path)
        db.save_project(project)
        project.path = path
        return path

    def open(self, path: Path) -> EngineeringProject:
        """Load open for the third Omega integrated product release while preserving typed state."""
        return ProjectDatabase(path).load_project()

    def snapshot(self, project: EngineeringProject, label: str) -> int:
        """Execute the public ProjectRepository.snapshot operation for the third Omega integrated product release using explicit caller inputs."""
        if project.path is None:
            raise ValueError("Project has no database path.")
        return ProjectDatabase(project.path).create_snapshot(project, label)
