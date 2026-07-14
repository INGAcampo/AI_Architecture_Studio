"""
AI Architecture Studio
Application Core

SNAP Professional v2
"""

from core.history.history_manager import HistoryManager
from core.layers.layer_manager import LayerManager
from core.logger import logger
from core.project_manager import ProjectManager
from core.scene_manager import SceneManager
from engines.cad.ortho import OrthoManager
from engines.cad.snap import SnapEngine
from kernel.application import AIASKernel


class AIASApplication:

    def __init__(self):
        logger.info(
            "Inicializando AIAS..."
        )

        self.kernel = AIASKernel()

        self.layer_manager = LayerManager()
        self.ortho_manager = OrthoManager()
        self.snap_engine = SnapEngine()
        self.project_manager = ProjectManager()

        self.kernel.services.register(
            "layer_manager",
            self.layer_manager,
        )

        self.kernel.services.register(
            "ortho_manager",
            self.ortho_manager,
        )

        self.kernel.services.register(
            "snap_engine",
            self.snap_engine,
        )

        self.scene = SceneManager(
            kernel=self.kernel
        )

        self.history = HistoryManager()

        self.kernel.services.register(
            "project_manager",
            self.project_manager,
        )

        self.kernel.services.register(
            "scene_manager",
            self.scene,
        )

        self.kernel.services.register(
            "history_manager",
            self.history,
        )

        if (
            self.kernel.services.get(
                "layer_manager"
            )
            is not self.layer_manager
        ):
            raise RuntimeError(
                "LayerManager no se registró "
                "correctamente en el kernel"
            )

        if (
            self.kernel.services.get(
                "snap_engine"
            )
            is not self.snap_engine
        ):
            raise RuntimeError(
                "SnapEngine no se registró "
                "correctamente en el kernel"
            )

        logger.info(
            "Kernel, historial, capas, ORTHO "
            "y SNAP conectados correctamente."
        )

    def start(self):
        logger.info(
            "AIAS iniciado correctamente."
        )

        logger.info(
            self.kernel.info()
        )

    def new_scene(self):
        self.scene = SceneManager(
            kernel=self.kernel
        )

        self.history = HistoryManager()

        self.kernel.services.register(
            "scene_manager",
            self.scene,
        )

        self.kernel.services.register(
            "history_manager",
            self.history,
        )

        self.kernel.services.register(
            "layer_manager",
            self.layer_manager,
        )

        self.kernel.services.register(
            "ortho_manager",
            self.ortho_manager,
        )

        self.kernel.services.register(
            "snap_engine",
            self.snap_engine,
        )

        logger.info(
            "Nueva escena e historial creados."
        )

    def scene_summary(self):
        return self.scene.summary()