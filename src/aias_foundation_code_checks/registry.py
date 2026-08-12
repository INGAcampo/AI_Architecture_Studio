"""In-memory registry for uniquely identified and serialized engineering code packs."""
from __future__ import annotations
from dataclasses import asdict
from pathlib import Path
import json
from .models import CodePack

class CodePackRegistry:
    """Register, retrieve, list and load code packs without silent replacement."""
    def __init__(self):
        self._packs: dict[str, CodePack] = {}

    def register(self, pack: CodePack) -> None:
        """Register a uniquely identified pack and reject silent replacement."""
        if pack.code_id in self._packs:
            raise ValueError("duplicate_code_pack")
        self._packs[pack.code_id] = pack

    def get(self, code_id: str) -> CodePack:
        """Return a registered pack or raise for an unknown identity."""
        if code_id not in self._packs:
            raise KeyError(code_id)
        return self._packs[code_id]

    def list_ids(self) -> list[str]:
        """Return registered code-pack identities in deterministic order."""
        return sorted(self._packs)

    def load_json(self, path: Path) -> CodePack:
        """Load a JSON pack, construct its typed record and register it."""
        pack=CodePack(**json.loads(path.read_text(encoding="utf-8")))
        self.register(pack)
        return pack
