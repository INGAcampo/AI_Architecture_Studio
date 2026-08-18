"""CAD layer state and unique layer management."""
from dataclasses import dataclass

@dataclass(slots=True)
class Layer:
    """Named drawing layer with color, visibility and lock state."""
    name: str
    visible: bool = True
    frozen: bool = False
    locked: bool = False
    lineweight: float = 0.25

class LayerEngine:
    """Create, select and control layers without duplicate names."""
    def __init__(self) -> None:
        self._layers={"0":Layer("0")}
        self.current="0"

    def create(self, name: str) -> Layer:
        """Build the create required by the S1 professional CAD foundation program from explicit inputs."""
        if name in self._layers:
            raise ValueError(name)
        layer=Layer(name)
        self._layers[name]=layer
        return layer

    def set_current(self, name: str) -> None:
        """Execute set current for the S1 professional CAD foundation program with validated state transitions."""
        if name not in self._layers: raise KeyError(name)
        self.current=name

    def get(self, name: str) -> Layer:
        """Return get from the S1 professional CAD foundation program using deterministic lookup rules."""
        return self._layers[name]

    def all(self):
        """Execute the public LayerEngine.all operation for the S1 professional CAD foundation program using explicit caller inputs."""
        return tuple(self._layers.values())
