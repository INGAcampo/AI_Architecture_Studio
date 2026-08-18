from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RoundtripGuard:
    semantic_identity_preserved: bool
    geometry_identity_preserved: bool
    composite_identity_preserved: bool

    @property
    def passed(self) -> bool:
        return (
            self.semantic_identity_preserved
            and self.geometry_identity_preserved
            and self.composite_identity_preserved
        )


def evaluate_roundtrip_identity(before, after) -> RoundtripGuard:
    return RoundtripGuard(
        semantic_identity_preserved=before.semantic_key == after.semantic_key,
        geometry_identity_preserved=before.geometry_key == after.geometry_key,
        composite_identity_preserved=before.composite_key == after.composite_key,
    )
