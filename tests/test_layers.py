import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from core.layers.layer_manager import LayerManager
from engines.cad.renderer import Renderer
from engines.geometry.line import Line
from engines.geometry.point import Point
from engines.selection.hit_test import HitTest


class DummyPainter:
    def __init__(self):
        self.calls = []

    def setPen(self, pen):
        self.calls.append(("setPen", pen))

    def drawLine(self, x1, y1, x2, y2):
        self.calls.append(("drawLine", x1, y1, x2, y2))

    def drawEllipse(self, x1, y1, x2, y2):
        self.calls.append(("drawEllipse", x1, y1, x2, y2))


class DummyScene:
    def __init__(self, elements, layer_manager):
        self._elements = elements
        self.kernel = SimpleNamespace(
            services=SimpleNamespace(get=lambda name: layer_manager)
        )

    def get_elements(self):
        return self._elements


class DummyElement:
    def __init__(self, layer_name, geometry):
        self.layer_name = layer_name
        self.geometry = geometry
        self.name = "dummy"


def _build_scene(layer_name, layer_manager):
    element = DummyElement(
        layer_name=layer_name,
        geometry=Line(Point(0, 0, 0), Point(1, 0, 0)),
    )
    return DummyScene([element], layer_manager), element


def test_hidden_layer_is_not_rendered():
    renderer = Renderer()
    layer_manager = LayerManager()
    layer_manager.create_layer("hidden")
    layer_manager.set_visibility("hidden", False)

    scene, _ = _build_scene("hidden", layer_manager)
    painter = DummyPainter()

    renderer.draw_scene(painter, camera=SimpleNamespace(zoom=1), scene=scene)

    assert painter.calls == []


def test_hidden_layer_is_not_selected():
    layer_manager = LayerManager()
    layer_manager.create_layer("hidden")
    layer_manager.set_visibility("hidden", False)

    scene, element = _build_scene("hidden", layer_manager)

    picked = HitTest.pick(Point(0.1, 0.0, 0.0), scene, tolerance=0.2)

    assert picked is None


def test_locked_layer_is_not_selected():
    layer_manager = LayerManager()
    layer_manager.create_layer("locked")
    layer_manager.set_locked("locked", True)

    scene, _ = _build_scene("locked", layer_manager)

    picked = HitTest.pick(Point(0.1, 0.0, 0.0), scene, tolerance=0.2)

    assert picked is None


def test_visible_unlocked_layer_is_selected():
    layer_manager = LayerManager()
    layer_manager.create_layer("visible")
    layer_manager.set_visibility("visible", True)
    layer_manager.set_locked("visible", False)

    scene, element = _build_scene("visible", layer_manager)

    picked = HitTest.pick(Point(0.1, 0.0, 0.0), scene, tolerance=0.2)

    assert picked is element


def test_toggle_visibility_changes_layer_state():
    layer_manager = LayerManager()
    layer_manager.create_layer("toggle_vis")
    layer = layer_manager.get_layer("toggle_vis")

    assert layer.visible is True

    layer_manager.set_visibility("toggle_vis", not layer.visible)

    assert layer_manager.get_layer("toggle_vis").visible is False


def test_toggle_locked_changes_layer_state():
    layer_manager = LayerManager()
    layer_manager.create_layer("toggle_lock")
    layer = layer_manager.get_layer("toggle_lock")

    assert layer.locked is False

    layer_manager.set_locked("toggle_lock", not layer.locked)

    assert layer_manager.get_layer("toggle_lock").locked is True
