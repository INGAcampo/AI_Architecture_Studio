from dataclasses import dataclass
from cad_professional_kernel.geometry import Point2D

@dataclass(slots=True)
class CommandState:
    active_command: str = ""
    prompt: str = "Comando:"
    first_point: Point2D | None = None
    preview_point: Point2D | None = None

    def begin(self, command: str, prompt: str) -> None:
        self.active_command=command
        self.prompt=prompt
        self.first_point=None
        self.preview_point=None

    def cancel(self) -> None:
        self.active_command=""
        self.prompt="Comando:"
        self.first_point=None
        self.preview_point=None
