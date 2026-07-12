"""
AI Architecture Studio
Application Core

Foundation 3.2
"""

from core.history.history_manager import HistoryManager
from core.logger import logger
from core.project_manager import ProjectManager
from core.scene_manager import SceneManager
from kernel.application import AIASKernel


class AIASApplication:

    def __init__(self):
        logger.info("Inicializando AIAS...")

        self.kernel = AIASKernel()

        self.project_manager = ProjectManager()
        self.scene = SceneManager(kernel=self.kernel)
        self.history = HistoryManager()

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

        logger.info("Kernel e historial AIAS conectados correctamente.")

    def start(self):
        logger.info("AIAS iniciado correctamente.")
        logger.info(self.kernel.info())

    def new_scene(self):
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

        logger.info("Nueva escena e historial creados.")

    def scene_summary(self):
        return self.scene.summary()