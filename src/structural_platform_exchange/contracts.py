from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StructuralResultRecord:
    object_id: str
    result_type: str
    value: float
    unit: str
    case_name: str

    def validate(self) -> None:
        if not self.object_id.strip():
            raise ValueError("object_id must not be empty")
        if not self.result_type.strip():
            raise ValueError("result_type must not be empty")
        if not self.unit.strip():
            raise ValueError("unit must not be empty")
        if not self.case_name.strip():
            raise ValueError("case_name must not be empty")


@dataclass(frozen=True)
class StructuralExchangeEnvelope:
    schema_version: str
    source_engine: str
    model_id: str
    results: tuple[StructuralResultRecord,...]

    def validate(self) -> None:
        if not self.schema_version.strip():
            raise ValueError("schema_version must not be empty")
        if not self.source_engine.strip():
            raise ValueError("source_engine must not be empty")
        if not self.model_id.strip():
            raise ValueError("model_id must not be empty")

        for item in self.results:
            item.validate()
