"""Public module supporting the Omega application core and shared runtime services."""
from __future__ import annotations
from dataclasses import dataclass
from uuid import UUID, uuid4

@dataclass(frozen=True, slots=True)
class ObjectId:
    """Execute the public ObjectId operation for the Omega application core and shared runtime services using explicit caller inputs."""
    value: UUID

    @classmethod
    def new(cls) -> "ObjectId":
        """Build the new required by the Omega application core and shared runtime services from explicit inputs."""
        return cls(uuid4())

    @classmethod
    def parse(cls, value: str) -> "ObjectId":
        """Execute the public ObjectId.parse operation for the Omega application core and shared runtime services using explicit caller inputs."""
        return cls(UUID(value))

    def __str__(self) -> str:
        return str(self.value)
