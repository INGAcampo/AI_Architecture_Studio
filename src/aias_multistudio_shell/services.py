"""Public module supporting the coordinated multi-studio desktop shell."""
from dataclasses import dataclass
from .documents import DocumentManager
from .events import EventBus
from .project_model import AiasProject
from .studios import StudioRegistry

@dataclass(slots=True)
class ShellServices:
    """Execute the public ShellServices operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
    events: EventBus
    documents: DocumentManager
    studios: StudioRegistry
    project: AiasProject

    @classmethod
    def create_default(cls) -> "ShellServices":
        """Build the default required by the coordinated multi-studio desktop shell from explicit inputs."""
        return cls(
            events=EventBus(),
            documents=DocumentManager(),
            studios=StudioRegistry(),
            project=AiasProject("Untitled Project"),
        )
