from dataclasses import dataclass
from enum import Enum

class Discipline(str, Enum):
    ARCHITECTURE = "architecture"
    STRUCTURE = "structure"
    MEP = "mep"
    CIVIL = "civil"

@dataclass(frozen=True, slots=True)
class FederatedModel:
    model_id: str
    name: str
    discipline: Discipline
    revision: int
    source_uri: str = ""

    def __post_init__(self):
        if not self.model_id.strip() or not self.name.strip() or self.revision < 0:
            raise ValueError("Datos inválidos")

class BimCollaborationManager:
    def __init__(self):
        self._models = {}

    def register(self, model):
        current = self._models.get(model.model_id)
        if current is not None and model.revision < current.revision:
            raise ValueError("No se permite reducir la revisión")
        self._models[model.model_id] = model
        return model

    def federated_models(self):
        return tuple(self._models[key] for key in sorted(self._models))

    def latest_revision(self):
        return max((model.revision for model in self._models.values()), default=0)

    def by_discipline(self, discipline):
        return tuple(model for model in self._models.values() if model.discipline is discipline)
