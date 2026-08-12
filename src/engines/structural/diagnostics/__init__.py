from dataclasses import dataclass
from enum import Enum

class DiagnosticSeverity(str, Enum):
    INFO="info"
    WARNING="warning"
    ERROR="error"

@dataclass(frozen=True, slots=True)
class Diagnostic:
    code: str
    severity: DiagnosticSeverity
    message: str
    object_id: str | None = None
    def __post_init__(self):
        if not self.code.strip() or not self.message.strip():
            raise ValueError("Datos obligatorios")

class StructuralDiagnostics:
    def check_unconnected_nodes(self, node_ids, connected_node_ids):
        missing = sorted(set(node_ids) - set(connected_node_ids))
        return tuple(Diagnostic("UNCONNECTED_NODE", DiagnosticSeverity.ERROR, "Nodo no conectado", node_id) for node_id in missing)
    def check_singular_diagonal(self, matrix, tolerance=1e-12):
        return tuple(
            Diagnostic("ZERO_DIAGONAL", DiagnosticSeverity.ERROR, "Rigidez diagonal nula", str(i))
            for i, row in enumerate(matrix) if abs(row[i]) <= tolerance
        )
