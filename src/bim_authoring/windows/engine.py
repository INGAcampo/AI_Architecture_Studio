from .geometry import WindowGeometryBuilder
from .hosting import WindowHostAdapter
from .quantities import WindowQuantityEngine
from .regeneration import WindowRegenerationEngine
from .validation import WindowValidator

class NativeBimWindowEngine:
    def __init__(self, wall_engine=None):
        self.families = {}
        self.windows = {}
        self.wall_engine = wall_engine
        self.geometry_builder = WindowGeometryBuilder()
        self.quantity_engine = WindowQuantityEngine()
        self.validator = WindowValidator()
        self.host_adapter = WindowHostAdapter()
        self.regenerator = WindowRegenerationEngine(
            self.geometry_builder,
            self.quantity_engine,
            self.validator,
        )

    def register_family(self, family):
        self.families[family.family_id] = family
        return family

    def add_window(self, window, *, auto_host=True):
        if window.family_id not in self.families:
            raise KeyError(window.family_id)
        self.windows[window.window_id] = window
        if auto_host and self.wall_engine is not None:
            from bim_authoring.walls import WallOpening
            self.host_adapter.host(window, self.wall_engine, WallOpening)
        return window

    def update_window(self, window):
        if window.window_id not in self.windows:
            raise KeyError(window.window_id)
        self.windows[window.window_id] = window
        return self.regenerate(window.window_id)

    def regenerate(self, window_id):
        window = self.windows[window_id]
        wall = None
        if self.wall_engine is not None:
            wall = self.wall_engine.walls.get(window.host_wall_id)
        return self.regenerator.regenerate(window, wall)

    def quantities(self, window_id, *, delta_temperature=1.0):
        return self.quantity_engine.calculate(
            self.windows[window_id],
            delta_temperature=delta_temperature,
        )
