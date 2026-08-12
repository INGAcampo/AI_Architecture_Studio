from __future__ import annotations
from dataclasses import dataclass
import ast
import math
from typing import Mapping, Any


class FormulaError(ValueError):
    pass


_ALLOWED_FUNCTIONS = {
    "abs": abs,
    "min": min,
    "max": max,
    "round": round,
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "radians": math.radians,
    "degrees": math.degrees,
}


class _FormulaValidator(ast.NodeVisitor):
    _allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Constant,
        ast.Name,
        ast.Load,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Pow,
        ast.Mod,
        ast.USub,
        ast.UAdd,
        ast.Call,
    )

    def generic_visit(self, node):
        if not isinstance(node, self._allowed_nodes):
            raise FormulaError(f"Nodo no permitido: {type(node).__name__}")
        super().generic_visit(node)

    def visit_Call(self, node: ast.Call):
        if not isinstance(node.func, ast.Name):
            raise FormulaError("Solo se permiten funciones simples")
        if node.func.id not in _ALLOWED_FUNCTIONS:
            raise FormulaError(f"Función no permitida: {node.func.id}")
        self.generic_visit(node)


@dataclass(frozen=True, slots=True)
class Formula:
    target_parameter_id: str
    expression: str

    def __post_init__(self) -> None:
        if not self.target_parameter_id.strip():
            raise ValueError("target_parameter_id es obligatorio")
        if not self.expression.strip():
            raise ValueError("expression es obligatoria")
        tree = ast.parse(self.expression, mode="eval")
        _FormulaValidator().visit(tree)

    def dependencies(self) -> tuple[str, ...]:
        tree = ast.parse(self.expression, mode="eval")
        names = {
            node.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Name)
            and node.id not in _ALLOWED_FUNCTIONS
        }
        return tuple(sorted(names))

    def evaluate(self, values: Mapping[str, Any]) -> Any:
        missing = [
            dependency
            for dependency in self.dependencies()
            if dependency not in values
        ]
        if missing:
            raise FormulaError(
                "Faltan dependencias: " + ", ".join(missing)
            )
        scope = dict(_ALLOWED_FUNCTIONS)
        scope.update(values)
        try:
            return eval(
                compile(ast.parse(self.expression, mode="eval"), "<formula>", "eval"),
                {"__builtins__": {}},
                scope,
            )
        except Exception as exc:
            raise FormulaError(str(exc)) from exc
