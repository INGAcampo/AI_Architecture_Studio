"""
AI Architecture Studio
Layer Manager
"""

from core.layers.layer import Layer


class LayerManager:
    def __init__(self):
        self._layers = {}
        self._current_layer = None
        self.create_layer("0")

    @property
    def current_layer(self):
        return self._current_layer

    def create_layer(self, name, color="#DADADA", visible=True, locked=False, line_weight=1):
        if not name:
            raise ValueError("El nombre de la capa no puede estar vacío")

        if name in self._layers:
            return self._layers[name]

        layer = Layer(
            name=name,
            color=color,
            visible=visible,
            locked=locked,
            line_weight=line_weight,
        )
        self._layers[name] = layer

        if self._current_layer is None:
            self._current_layer = layer

        return layer

    def remove_layer(self, name):
        if name == "0":
            return False

        layer = self._layers.pop(name, None)
        if layer is None:
            return False

        if self._current_layer is layer:
            self._current_layer = self.get_layer("0")

        return True

    def get_layer(self, name):
        return self._layers.get(name)

    def set_current_layer(self, name):
        layer = self.get_layer(name)
        if layer is None:
            raise KeyError(f"La capa '{name}' no existe")
        self._current_layer = layer
        return layer

    def set_visibility(self, name, visible):
        layer = self.get_layer(name)
        if layer is None:
            raise KeyError(f"La capa '{name}' no existe")
        layer.visible = visible
        return layer

    def set_locked(self, name, locked):
        layer = self.get_layer(name)
        if layer is None:
            raise KeyError(f"La capa '{name}' no existe")
        layer.locked = locked
        return layer

    def all_layers(self):
        return list(self._layers.values())
