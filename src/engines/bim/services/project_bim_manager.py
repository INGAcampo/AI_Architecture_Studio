"""Enlace ligero entre un proyecto AIAS y su servicio BIM."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .bim_service import BimService


class ProjectBimManager:
    SERVICE_NAME = "bim_service"

    def __init__(
        self,
        *,
        project_path: str | Path | None = None,
        event_bus: Any | None = None,
        service_locator: Any | None = None,
    ) -> None:
        self.project_path = Path(project_path) if project_path else None
        self.service = BimService(event_bus=event_bus)
        self.service_locator = service_locator

        if service_locator is not None:
            register = getattr(service_locator, "register", None)
            if callable(register):
                register(self.SERVICE_NAME, self.service)

    @property
    def default_bim_path(self) -> Path | None:
        if self.project_path is None:
            return None
        if self.project_path.suffix:
            return self.project_path.with_suffix(".bim.json")
        return self.project_path / "model.bim.json"

    def save(self, path: str | Path | None = None) -> Path:
        target = Path(path) if path is not None else self.default_bim_path
        if target is None:
            raise ValueError("Debe indicarse una ruta para guardar BIM.")
        return self.service.save(target)

    def load(self, path: str | Path | None = None):
        source = Path(path) if path is not None else self.default_bim_path
        if source is None:
            raise ValueError("Debe indicarse una ruta para cargar BIM.")
        return self.service.load(source)
