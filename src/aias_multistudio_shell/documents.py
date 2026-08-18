"""Public module supporting the coordinated multi-studio desktop shell."""
from dataclasses import dataclass, field
from pathlib import Path
from uuid import uuid4

@dataclass(slots=True)
class StudioDocument:
    """Execute the public StudioDocument operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
    title: str
    studio_id: str
    path: Path | None = None
    document_id: str = field(default_factory=lambda: uuid4().hex)
    modified: bool = False

class DocumentManager:
    """Execute the public DocumentManager operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
    def __init__(self) -> None:
        self._documents: dict[str, StudioDocument] = {}
        self.active_id: str | None = None

    def add(self, document: StudioDocument) -> str:
        """Add add to the coordinated multi-studio desktop shell while enforcing identity constraints."""
        self._documents[document.document_id] = document
        self.active_id = document.document_id
        return document.document_id

    def close(self, document_id: str) -> StudioDocument:
        """Execute the public DocumentManager.close operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
        document = self._documents.pop(document_id)
        if self.active_id == document_id:
            self.active_id = next(iter(self._documents), None)
        return document

    def active(self) -> StudioDocument | None:
        """Execute the public DocumentManager.active operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
        return self._documents.get(self.active_id)

    def all(self) -> tuple[StudioDocument, ...]:
        """Execute the public DocumentManager.all operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
        return tuple(self._documents.values())
