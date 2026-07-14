"""
AI Architecture Studio
Application Core

Foundation 3.2
"""

from engines.cad.ortho import OrthoManager
from core.history.history_manager import HistoryManager
from core.layers.layer_manager import LayerManager
from engines.cad.ortho import OrthoManager
from core.logger import logger
from core.project_manager import ProjectManager
from core.scene_manager import SceneManager
from kernel.application import AIASKernel


class AIASApplication:

    def __init__(self):
        logger.info("Inicializando AIAS...")

        self.kernel = AIASKernel()

        self.project_manager = ProjectManager()
        self.layer_manager = LayerManager()
        self.kernel.services.register(
            "layer_manager",
            self.layer_manager
        )
        self.scene = SceneManager(kernel=self.kernel)
        self.history = HistoryManager()
        self.ortho_manager = OrthoManager()

        self.kernel.services.register(
            "project_manager",
            self.project_manager
        )
        self.kernel.services.register(
            "scene_manager",
            self.scene
        )
        self.kernel.services.register(
            "history_manager",
            self.history
        )
        self.kernel.services.register(
            "ortho_manager",
            self.ortho_manager
        )

        if self.kernel.services.get("layer_manager") is not self.layer_manager:
            raise RuntimeError("LayerManager no se registró correctamente en el kernel")

        logger.info("Kernel e historial AIAS conectados correctamente.")

    def start(self):
        logger.info("AIAS iniciado correctamente.")
        logger.info(self.kernel.info())

    def new_scene(self):
        if not hasattr(self, "layer_manager") or self.layer_manager is None:
            self.layer_manager = LayerManager()
            self.kernel.services.register(
                "layer_manager",
                self.layer_manager
            )

        self.scene = SceneManager(kernel=self.kernel)
        self.history = HistoryManager()

        self.kernel.services.register(
            "scene_manager",
            self.scene
        )
        self.kernel.services.register(
            "history_manager",
            self.history
        )
        self.kernel.services.register(
            "layer_manager",
            self.layer_manager
        )
        
        self.ortho_manager = OrthoManager()

        self.kernel.services.register(
            "ortho_manager",
            self.ortho_manager
        )

        if self.kernel.services.get("layer_manager") is not self.layer_manager:
            raise RuntimeError("LayerManager no se registró correctamente en el kernel")

        logger.info("Nueva escena e historial creados.")

    def scene_summary(self):
        return self.scene.summary()