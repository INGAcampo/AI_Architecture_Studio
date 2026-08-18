"""Public module supporting advanced AEPS production, governance and observability."""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
import shutil

@dataclass(slots=True)
class FileTransaction:
    """Execute the public FileTransaction operation for advanced AEPS production, governance and observability using explicit caller inputs."""
    root: Path
    backup: Path
    committed: bool = False
    created_paths: list[Path] = field(default_factory=list)

    def begin(self) -> None:
        """Execute the public FileTransaction.begin operation for advanced AEPS production, governance and observability using explicit caller inputs."""
        if self.backup.exists():
            shutil.rmtree(self.backup)
        if self.root.exists():
            shutil.copytree(self.root, self.backup)

    def track(self, path: Path) -> None:
        """Execute the public FileTransaction.track operation for advanced AEPS production, governance and observability using explicit caller inputs."""
        self.created_paths.append(path)

    def commit(self) -> None:
        """Execute the public FileTransaction.commit operation for advanced AEPS production, governance and observability using explicit caller inputs."""
        self.committed = True
        if self.backup.exists():
            shutil.rmtree(self.backup)

    def rollback(self) -> None:
        """Execute the public FileTransaction.rollback operation for advanced AEPS production, governance and observability using explicit caller inputs."""
        if self.root.exists():
            shutil.rmtree(self.root)
        if self.backup.exists():
            shutil.copytree(self.backup, self.root)
            shutil.rmtree(self.backup)
        self.committed = False
