from __future__ import annotations

import json
from typing import Any

from .collection import ParameterCollection
from .registry import ParameterDefinitionRegistry


class ParameterSerializer:
    def dumps(self, collection: ParameterCollection) -> str:
        return json.dumps(collection.snapshot(), ensure_ascii=False, indent=2, sort_keys=True)

    def loads(
        self,
        text: str,
        registry: ParameterDefinitionRegistry,
    ) -> ParameterCollection:
        data = json.loads(text)
        if not isinstance(data, dict):
            raise ValueError("El contenido debe ser un objeto JSON")

        collection = ParameterCollection(str(data["owner_id"]))
        values = data.get("values", {})
        for parameter_id, payload in values.items():
            definition = registry.get(parameter_id)
            value = collection.add_definition(
                definition,
                initial_value=payload.get("value"),
                source=str(payload.get("source", "import")),
            )
            value.revision = int(payload.get("revision", 0))
            value.error = payload.get("error")
        collection.revision = int(data.get("revision", collection.revision))
        return collection
