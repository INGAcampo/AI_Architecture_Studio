"""Public module supporting the coordinated multi-studio desktop shell."""
from dataclasses import dataclass
from typing import Callable, Any

@dataclass(frozen=True, slots=True)
class StudioDescriptor:
    """Execute the public StudioDescriptor operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
    studio_id: str
    name: str
    category: str
    factory: Callable[[], Any]
    description: str = ""

class StudioRegistry:
    """Execute the public StudioRegistry operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
    def __init__(self) -> None:
        self._studios: dict[str, StudioDescriptor] = {}

    def register(self, descriptor: StudioDescriptor) -> None:
        """Add register to the coordinated multi-studio desktop shell while enforcing identity constraints."""
        if descriptor.studio_id in self._studios:
            raise ValueError(f"Studio already registered: {descriptor.studio_id}")
        self._studios[descriptor.studio_id] = descriptor

    def get(self, studio_id: str) -> StudioDescriptor:
        """Return get from the coordinated multi-studio desktop shell using deterministic lookup rules."""
        return self._studios[studio_id]

    def all(self) -> tuple[StudioDescriptor, ...]:
        """Execute the public StudioRegistry.all operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
        return tuple(sorted(self._studios.values(), key=lambda x: (x.category, x.name)))

    def categories(self) -> tuple[str, ...]:
        """Execute the public StudioRegistry.categories operation for the coordinated multi-studio desktop shell using explicit caller inputs."""
        return tuple(sorted({x.category for x in self._studios.values()}))
