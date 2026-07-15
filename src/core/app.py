"""
AI Architecture Studio
Application Core

Dynamic Input v2
"""

from core.history.history_manager import HistoryManager
from core.layers.layer_manager import LayerManager
from core.logger import logger
from core.project_manager import ProjectManager
from core.scene_manager import SceneManager
from engines.cad.dynamic_input import DynamicInputManager
from engines.cad.ortho import OrthoManager
from engines.cad.snap import SnapEngine
from kernel.application import AIASKernel


class AIASApplication:

    def __init__(self):
        logger.info("Inicializando AIAS...")

        self.kernel = AIASKernel()

        self.layer_manager = LayerManager()
        self.ortho_manager = OrthoManager()
        self.snap_engine = SnapEngine()
        self.dynamic_input_manager = DynamicInputManager()
        self.project_manager = ProjectManager()

        self.kernel.services.register("layer_manager", self.layer_manager)
        self.kernel.services.register("ortho_manager", self.ortho_manager)
        self.kernel.services.register("snap_engine", self.snap_engine)
        self.kernel.services.register(
            "dynamic_input_manager",
            self.dynamic_input_manager,
        )

        self.scene = SceneManager(kernel=self.kernel)
        self.history = HistoryManager()

        self.kernel.services.register("project_manager", self.project_manager)
        self.kernel.services.register("scene_manager", self.scene)
        self.kernel.services.register("history_manager", self.history)

        self._validate_services()

        logger.info(
            "Kernel, historial, capas, ORTHO, SNAP "
            "y Dynamic Input conectados correctamente."
        )

    def _validate_services(self):
        services = {
            "layer_manager": self.layer_manager,
            "ortho_manager": self.ortho_manager,
            "snap_engine": self.snap_engine,
            "dynamic_input_manager": self.dynamic_input_manager,
            "project_manager": self.project_manager,
            "scene_manager": self.scene,
            "history_manager": self.history,
        }

        for service_name, expected_instance in services.items():
            registered_instance = self.kernel.services.get(service_name)

            if registered_instance is not expected_instance:
                raise RuntimeError(
                    f"{service_name} no se registró "
                    "correctamente en el kernel"
                )

    def start(self):
        logger.info("AIAS iniciado correctamente.")
        logger.info(self.kernel.info())

    def new_scene(self):
        self.scene = SceneManager(kernel=self.kernel)
        self.history = HistoryManager()

        self.dynamic_input_manager.reset()

        self.kernel.services.register("scene_manager", self.scene)
        self.kernel.services.register("history_manager", self.history)
        self.kernel.services.register("layer_manager", self.layer_manager)
        self.kernel.services.register("ortho_manager", self.ortho_manager)
        self.kernel.services.register("snap_engine", self.snap_engine)
        self.kernel.services.register(
            "dynamic_input_manager",
            self.dynamic_input_manager,
        )

        self._validate_services()

        logger.info("Nueva escena e historial creados.")

    def scene_summary(self):
        return self.scene.summary()