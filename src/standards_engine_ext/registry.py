from __future__ import annotations

from .provenance import RulePack, verify_rule_pack


class RulePackRegistry:
    def __init__(self) -> None:
        self._packs={}

    def register(self, pack: RulePack) -> None:
        if not verify_rule_pack(pack):
            raise ValueError("rule pack provenance/hash validation failed")

        key=(pack.pack_id,pack.version)
        if key in self._packs:
            raise ValueError("rule pack version already registered")

        self._packs[key]=pack

    def get(self, pack_id: str, version: str) -> RulePack:
        return self._packs[(pack_id,version)]

    @property
    def count(self) -> int:
        return len(self._packs)
