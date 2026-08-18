"""Gestión central del documento activo de AIAS."""
from __future__ import annotations

from pathlib import Path
from typing import Any


class DocumentManager:
    def __init__(self, event_bus=None):
        self.event_bus = event_bus
        self.current_document: Any = None

    @property
    def has_document(self) -> bool:
        return self.current_document is not None

    @property
    def file_path(self) -> Path | None:
        if self.current_document is None:
            return None
        value = getattr(self.current_document, "file_path", None)
        return Path(value) if value else None

    @property
    def is_dirty(self) -> bool:
        return bool(
            self.current_document is not None
            and getattr(self.current_document, "dirty", False)
        )

    def set_document(self, document):
        previous = self.current_document
        self.current_document = document
        self._emit(
            "document.changed",
            {"previous": previous, "document": document},
        )
        return document

    def mark_dirty(self):
        if self.current_document is None:
            return False
        marker = getattr(self.current_document, "mark_dirty", None)
        if callable(marker):
            marker()
        else:
            self.current_document.dirty = True
        self._emit("document.dirty_changed", True)
        return True

    def mark_clean(self):
        if self.current_document is None:
            return False
        marker = getattr(self.current_document, "mark_clean", None)
        if callable(marker):
            marker()
        else:
            self.current_document.dirty = False
        self._emit("document.dirty_changed", False)
        return True

    def close_document(self):
        previous = self.current_document
        self.current_document = None
        self._emit("document.closed", previous)
        return previous

    def _emit(self, event_name, data=None):
        if self.event_bus is not None:
            self.event_bus.emit(event_name, data)
