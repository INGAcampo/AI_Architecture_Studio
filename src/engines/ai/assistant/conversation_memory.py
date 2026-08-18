from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True, slots=True)
class ConversationEntry:
    role: str
    content: str

    def __post_init__(self) -> None:
        if self.role not in {"user", "assistant", "system"}:
            raise ValueError("role inválido")
        if not self.content.strip():
            raise ValueError("content es obligatorio")


class ConversationMemory:
    def __init__(self, max_entries: int = 100) -> None:
        if max_entries < 1:
            raise ValueError("max_entries debe ser positivo")
        self.max_entries = max_entries
        self._entries: list[ConversationEntry] = []

    def add(self, role: str, content: str) -> ConversationEntry:
        entry = ConversationEntry(role, content)
        self._entries.append(entry)
        if len(self._entries) > self.max_entries:
            self._entries = self._entries[-self.max_entries:]
        return entry

    def all(self) -> tuple[ConversationEntry, ...]:
        return tuple(self._entries)

    def recent(self, limit: int = 10) -> tuple[ConversationEntry, ...]:
        if limit < 0:
            raise ValueError("limit inválido")
        return tuple(self._entries[-limit:])

    def clear(self) -> None:
        self._entries.clear()

    def __len__(self) -> int:
        return len(self._entries)

    def __iter__(self) -> Iterable[ConversationEntry]:
        return iter(self._entries)
