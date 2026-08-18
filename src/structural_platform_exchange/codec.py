from __future__ import annotations

import hashlib
import json

from .contracts import StructuralExchangeEnvelope, StructuralResultRecord


def encode_exchange_json(envelope: StructuralExchangeEnvelope) -> str:
    envelope.validate()

    data={
        "schema_version":envelope.schema_version,
        "source_engine":envelope.source_engine,
        "model_id":envelope.model_id,
        "results":[
            {
                "object_id":r.object_id,
                "result_type":r.result_type,
                "value":float(r.value),
                "unit":r.unit,
                "case_name":r.case_name,
            }
            for r in envelope.results
        ],
    }

    return json.dumps(
        data,
        sort_keys=True,
        separators=(",",":"),
        ensure_ascii=True,
    )


def decode_exchange_json(raw: str) -> StructuralExchangeEnvelope:
    data=json.loads(raw)

    envelope=StructuralExchangeEnvelope(
        schema_version=str(data["schema_version"]),
        source_engine=str(data["source_engine"]),
        model_id=str(data["model_id"]),
        results=tuple(
            StructuralResultRecord(
                object_id=str(item["object_id"]),
                result_type=str(item["result_type"]),
                value=float(item["value"]),
                unit=str(item["unit"]),
                case_name=str(item["case_name"]),
            )
            for item in data.get("results",[])
        ),
    )
    envelope.validate()
    return envelope


def exchange_sha256(envelope: StructuralExchangeEnvelope) -> str:
    return hashlib.sha256(
        encode_exchange_json(envelope).encode("ascii")
    ).hexdigest()
