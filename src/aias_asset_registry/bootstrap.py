"""Public module supporting the universal engineering asset registry."""
from __future__ import annotations

import json
from pathlib import Path

from .registry import AssetRegistry


STATE = {
    "PLANNED": "PROPOSED",
    "SPECIFIED": "SPECIFIED",
    "PARTIAL": "IMPLEMENTED",
    "OPERATIONAL": "OPERATED",
    "DUPLICATE": "RETIRED",
}


def ingest_master_inventory(
    inventory_path: Path,
    registry_path: Path,
) -> dict:
    """Ingest every governed concept from the current master inventory."""

    data = json.loads(inventory_path.read_text(encoding="utf-8"))
    registry = AssetRegistry(registry_path)

    rows = sorted(
        data["concepts"],
        key=lambda row: (row["wave"], row["id"]),
    )
    known = set(registry.data["assets"])

    for row in rows:
        if row["id"] in known:
            continue

        registry.register(
            {
                "id": row["id"],
                "title": row["name"],
                "asset_type": row["kind"],
                "version": "1.0.0",
                "status": STATE[row["declared_state"]],
                "owner": "AIAS_CORE_ENGINEERING",
                "purpose": row["name"],
                "scope": "AIAS",
                "source": row.get("evidence") or "MASTER_INVENTORY",
                "requirements": [],
                "evidence": (
                    [row["evidence"]]
                    if row.get("evidence_exists")
                    else []
                ),
                "dependencies": [
                    dependency
                    for dependency in row.get("depends_on", [])
                    if dependency in known
                ],
                "legal_status": "GOVERNED_REFERENCE",
            },
            "AMIR-000001",
        )
        known.add(row["id"])

    return {
        "ingested": len(registry.data["assets"]),
        "events": len(registry.data["events"]),
        "path": str(registry_path),
    }
