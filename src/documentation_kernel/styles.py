from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class GraphicStyle:
    style_id: str
    text_height: float = 2.5
    line_weight: float = 0.25
    font_family: str = "Arial"

    def __post_init__(self):
        if not self.style_id.strip():
            raise ValueError("style_id es obligatorio")
        if self.text_height <= 0 or self.line_weight <= 0:
            raise ValueError("Valores gráficos inválidos")

class StyleRegistry:
    def __init__(self):
        self._styles = {}

    def register(self, style, *, replace=False):
        if style.style_id in self._styles and not replace:
            raise ValueError(f"Estilo duplicado: {style.style_id}")
        self._styles[style.style_id] = style

    def get(self, style_id):
        return self._styles[style_id]

    def all(self):
        return tuple(self._styles[key] for key in sorted(self._styles))
