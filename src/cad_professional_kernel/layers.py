from __future__ import annotations
from dataclasses import dataclass

@dataclass(slots=True)
class Layer:
    name: str
    visible: bool = True
    locked: bool = False
    lineweight: float = 0.25

class LayerManager:
    def __init__(self) -> None:
        self._layers = {"0": Layer("0")}
        self.current = "0"

    def add(self, layer: Layer) -> None:
        if layer.name in self._layers:
            raise ValueError(f"Layer already exists: {layer.name}")
        self._layers[layer.name] = layer

    def get(self, name: str) -> Layer:
        return self._layers[name]

    def set_current(self, name: str) -> None:
        if name not in self._layers:
            raise KeyError(name)
        self.current = name

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._layers))
