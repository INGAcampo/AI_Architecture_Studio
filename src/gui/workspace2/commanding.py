"""Professional command search, capability gating and status truth for Workspace 2.0."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Iterable


class Availability(str, Enum):
    AVAILABLE = "AVAILABLE"
    REFERENCE_ONLY = "REFERENCE_ONLY"
    UNAVAILABLE = "UNAVAILABLE"


@dataclass(frozen=True)
class CommandDescriptor:
    command_id: str
    title: str
    aliases: tuple[str, ...]
    discipline: str
    capability_id: str
    availability: Availability = Availability.AVAILABLE
    requires_professional_review: bool = False
    description: str = ""
    handler: Callable[..., Any] | None = field(default=None, compare=False, repr=False)

    def __post_init__(self):
        if not self.command_id or not self.title or not self.capability_id:
            raise ValueError("invalid_command_descriptor")
        normalized = tuple(alias.strip().upper() for alias in self.aliases if alias.strip())
        if len(normalized) != len(set(normalized)):
            raise ValueError("duplicate_command_alias")
        object.__setattr__(self, "aliases", normalized)


@dataclass
class ProfessionalStatus:
    jurisdiction: str = "VE"
    units: str = "SI"
    normative_pack: str | None = None
    normative_status: str = "NOT_ACQUIRED"
    review_status: str = "DRAFT"
    professional_reviewer: str | None = None

    def snapshot(self) -> dict:
        return {
            "schema": "AIAS-PROFESSIONAL-STATUS-1.0",
            "jurisdiction": self.jurisdiction,
            "units": self.units,
            "normative_pack": self.normative_pack,
            "normative_status": self.normative_status,
            "review_status": self.review_status,
            "professional_reviewer": self.professional_reviewer,
            "engineering_release_authorized": self.normative_status == "VALIDATED" and self.review_status == "APPROVED" and bool(self.professional_reviewer),
        }


class CommandRegistry:
    def __init__(self):
        self._commands: dict[str, CommandDescriptor] = {}
        self._aliases: dict[str, str] = {}

    def register(self, command: CommandDescriptor) -> None:
        if command.command_id in self._commands:
            raise KeyError(f"duplicate_command_id:{command.command_id}")
        tokens = (command.command_id.upper(), *command.aliases)
        conflicts = [token for token in tokens if token in self._aliases]
        if conflicts:
            raise KeyError(f"command_alias_conflict:{','.join(conflicts)}")
        self._commands[command.command_id] = command
        for token in tokens:
            self._aliases[token] = command.command_id

    def resolve(self, token: str) -> CommandDescriptor:
        key = token.strip().upper()
        try:
            return self._commands[self._aliases[key]]
        except KeyError as exc:
            raise KeyError(f"unknown_command:{token}") from exc

    def search(self, query: str, *, discipline: str | None = None, limit: int = 12) -> tuple[CommandDescriptor, ...]:
        text = query.strip().casefold()
        ranked = []
        for command in self._commands.values():
            if discipline and command.discipline.casefold() != discipline.casefold():
                continue
            haystack = " ".join((command.command_id, command.title, command.description, command.discipline, *command.aliases)).casefold()
            if text and text not in haystack:
                continue
            exact = text in {command.command_id.casefold(), *(alias.casefold() for alias in command.aliases)}
            prefix = command.title.casefold().startswith(text) or command.command_id.casefold().startswith(text)
            score = (100 if exact else 0) + (30 if prefix else 0) + (10 if command.availability is Availability.AVAILABLE else 0)
            ranked.append((score, command.title.casefold(), command))
        ranked.sort(key=lambda item: (-item[0], item[1]))
        return tuple(item[2] for item in ranked[:max(0, limit)])

    def execute(self, token: str, *args, **kwargs):
        command = self.resolve(token)
        if command.availability is Availability.UNAVAILABLE:
            raise RuntimeError(f"capability_unavailable:{command.capability_id}")
        if command.availability is Availability.REFERENCE_ONLY:
            raise RuntimeError(f"reference_only_capability:{command.capability_id}")
        if command.handler is None:
            raise RuntimeError(f"command_handler_not_connected:{command.command_id}")
        return command.handler(*args, **kwargs)

    def all(self) -> tuple[CommandDescriptor, ...]:
        return tuple(self._commands[key] for key in sorted(self._commands))


def core_command_catalog(handlers: dict[str, Callable] | None = None, translator=None) -> CommandRegistry:
    handlers = handlers or {}
    rows = (
        ("LINE", "command.line", "Line", ("L", "LINEA"), "CAD", "CAD-LINE", Availability.AVAILABLE, False),
        ("WALL", "command.wall", "Wall", ("W", "MURO"), "Architecture", "BIM-WALL", Availability.AVAILABLE, False),
        ("ROOM", "command.room", "Room / Space", ("RM", "AMBIENTE"), "Architecture", "BIM-ROOM", Availability.AVAILABLE, False),
        ("SLAB", "command.slab", "Slab", ("LJ", "LOSA"), "Structure", "BIM-SLAB", Availability.AVAILABLE, False),
        ("STANDARDS", "command.standards", "Project Standards", ("NORMA", "NORMAS"), "Governance", "AEKS-STANDARDS", Availability.AVAILABLE, True),
        ("CAPABILITY-CENTER", "command.capability_center", "AIAS Capability Center", ("CAPACIDADES", "PLATAFORMA"), "Governance", "EXP-PLATFORM-GUI-001", Availability.AVAILABLE, False),
        ("STRUCTURAL-DESIGN", "command.structural_design", "Structural Design", ("DISENOESTRUCTURAL",), "Structure", "SCP-DESIGN", Availability.REFERENCE_ONLY, True),
        ("STRUCTURAL-REPORT", "command.structural_report", "Structural Calculation Report", ("MEMORIACALCULO",), "Structure", "SCP-REPORT", Availability.REFERENCE_ONLY, True),
        ("REVIT-SYNC", "command.revit_sync", "Revit Synchronization", ("REVIT",), "Interoperability", "INT-REVIT", Availability.UNAVAILABLE, False),
    )
    registry = CommandRegistry()
    for identifier, key, fallback, aliases, discipline, capability, availability, review in rows:
        title = translator.translate(key) if translator is not None else fallback
        registry.register(CommandDescriptor(identifier, title, aliases, discipline, capability, availability, review, handler=handlers.get(identifier)))
    return registry
