"""Persistencia JSON atómica para documentos BIM."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import NamedTemporaryFile

from ..document import BimDocument


class BimDocumentRepository:
    def save(self, document: BimDocument, path: str | Path) -> Path:
        target = Path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps(
            document.to_dict(),
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )

        with NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=target.parent,
            prefix=f".{target.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary.write(payload)
            temporary.write("\n")
            temporary_path = Path(temporary.name)

        temporary_path.replace(target)
        return target

    def load(self, path: str | Path) -> BimDocument:
        source = Path(path)
        if not source.exists():
            raise FileNotFoundError(source)
        data = json.loads(source.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise ValueError("El archivo BIM debe contener un objeto JSON.")
        return BimDocument.from_dict(data)
