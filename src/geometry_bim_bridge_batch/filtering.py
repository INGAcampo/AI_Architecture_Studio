from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VisibilityRule:
    entity_types: tuple[str,...] = ()
    global_ids: tuple[str,...] = ()
    hidden: bool = False


def matches_visibility_rule(payload, rule: VisibilityRule) -> bool:
    if rule.hidden:
        return False

    if rule.entity_types and payload.entity_type not in rule.entity_types:
        return False

    if rule.global_ids and payload.global_id not in rule.global_ids:
        return False

    return True
