"""
AI Architecture Studio
Application Core

Versión: 0.5.2 Alpha
"""
from __future__ import annotations

from core.document_manager import DocumentManager
from core.history.history_manager import HistoryManager
from core.layers.layer_manager import LayerManager
from core.logger import logger
from core.project_manager import ProjectManager
from core.scene_manager import SceneManager
from core.settings_manager import SettingsManager
from engines.cad.dynamic_input import DynamicInputManager
from engines.cad.ortho import OrthoManager
from engines.cad.snap import SnapEngine
from kernel.application import AIASKernel


class ApplicationCore:
    """Núcleo único de servicios y ciclo de vida de AIAS."""

    VERSION = "0.5.2-alpha"

    def __init__(self):
        logger.info("Inicializando ApplicationCore de AIAS...")

        self.kernel = AIASKernel()

        # Servicios persistentes durante toda la sesión.
        self.layer_manager = LayerManager()
        self.ortho_manager = OrthoManager()
        self.snap_engine = SnapEngine()
        self.dynamic_input_manager = DynamicInputManager()
        self.project_manager = ProjectManager()
        self.settings_manager = SettingsManager()
        self.document_manager = DocumentManager(
            event_bus=self.kernel.event_bus,
        )

        # Servicios dependientes del documento/escena.
        self.scene = SceneManager(kernel=self.kernel)
        self.history = HistoryManager()

        self._register_services()
        self._validate_services()

        logger.info(
            "ApplicationCore conectado: kernel, documento, escena, historial, "
            "capas, ORTHO, SNAP, Dynamic Input, ajustes y proyectos."
        )

    @property
    def event_bus(self):
        return self.kernel.event_bus

    @property
    def plugin_manager(self):
        return self.kernel.plugins

    @property
    def service_locator(self):
        return self.kernel.services

    @property
    def object_registry(self):
        return self.kernel.registry

    def _service_map(self):
        return {
            "application_core": self,
            "event_bus": self.event_bus,
            "object_registry": self.object_registry,
            "plugin_manager": self.plugin_manager,
            "layer_manager": self.layer_manager,
            "ortho_manager": self.ortho_manager,
            "snap_engine": self.snap_engine,
            "dynamic_input_manager": self.dynamic_input_manager,
            "project_manager": self.project_manager,
            "document_manager": self.document_manager,
            "settings_manager": self.settings_manager,
            "scene_manager": self.scene,
            "history_manager": self.history,
        }

    def _register_services(self):
        for name, service in self._service_map().items():
            self.kernel.services.register(name, service)

    def _validate_services(self):
        for name, expected in self._service_map().items():
            if self.kernel.services.get(name) is not expected:
                raise RuntimeError(
                    f"El servicio '{name}' no se registró correctamente."
                )

    def start(self):
        self.event_bus.emit("application.starting", self)
        logger.info("AIAS iniciado correctamente.")
        logger.info(self.kernel.info())
        self.event_bus.emit("application.started", self)

    def shutdown(self):
        self.event_bus.emit("application.stopping", self)
        self.settings_manager.save()
        logger.info("AIAS cerrado correctamente.")
        self.event_bus.emit("application.stopped", self)

    def new_scene(self):
        old_scene = self.scene
        self.scene = SceneManager(kernel=self.kernel)
        self.history = HistoryManager()
        self.dynamic_input_manager.reset()

        self.kernel.services.register("scene_manager", self.scene)
        self.kernel.services.register("history_manager", self.history)
        self._validate_services()

        payload = {"old_scene": old_scene, "scene": self.scene}
        self.event_bus.emit("application.scene_reset", payload)
        logger.info("Nueva escena e historial creados.")
        return self.scene

    def scene_summary(self):
        return self.scene.summary()


# Nombre histórico conservado para no romper imports existentes.
AIASApplication = ApplicationCore
