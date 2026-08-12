from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Any


_ALLOWED_BINARY = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.Pow: lambda a, b: a ** b,
    ast.Mod: lambda a, b: a % b,
}

_ALLOWED_UNARY = {
    ast.UAdd: lambda value: +value,
    ast.USub: lambda value: -value,
}

_ALLOWED_FUNCTIONS = {
    "abs": abs,
    "min": min,
    "max": max,
    "round": round,
}


@dataclass(frozen=True, slots=True)
class ParsedFormula:
    expression: str
    tree: ast.Expression
    dependencies: tuple[str, ...]


class SafeFormulaParser:
    def parse(self, expression: str) -> ParsedFormula:
        text = expression.strip()
        if not text:
            raise ValueError("La fórmula no puede estar vacía")
        tree = ast.parse(text, mode="eval")
        self._validate(tree)
        dependencies = tuple(sorted(self._collect_dependencies(tree)))
        return ParsedFormula(text, tree, dependencies)

    def evaluate(self, parsed: ParsedFormula, values: dict[str, Any]) -> Any:
        return self._eval_node(parsed.tree.body, values)

    def _validate(self, tree: ast.AST) -> None:
        for node in ast.walk(tree):
            if isinstance(node, (ast.Expression, ast.Load, ast.Constant, ast.Name)):
                continue
            if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINARY:
                continue
            if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARY:
                continue
            if isinstance(node, ast.Call):
                if not isinstance(node.func, ast.Name) or node.func.id not in _ALLOWED_FUNCTIONS:
                    raise ValueError("Función no permitida")
                if node.keywords:
                    raise ValueError("No se permiten argumentos con nombre")
                continue
            if isinstance(node, tuple(_ALLOWED_BINARY) + tuple(_ALLOWED_UNARY)):
                continue
            raise ValueError(f"Elemento no permitido en fórmula: {type(node).__name__}")

    def _collect_dependencies(self, tree: ast.AST) -> set[str]:
        return {
            node.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Name) and node.id not in _ALLOWED_FUNCTIONS
        }

    def _eval_node(self, node: ast.AST, values: dict[str, Any]) -> Any:
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Name):
            try:
                return values[node.id]
            except KeyError as exc:
                raise KeyError(f"Parámetro no definido: {node.id}") from exc
        if isinstance(node, ast.BinOp):
            operator = _ALLOWED_BINARY[type(node.op)]
            return operator(
                self._eval_node(node.left, values),
                self._eval_node(node.right, values),
            )
        if isinstance(node, ast.UnaryOp):
            operator = _ALLOWED_UNARY[type(node.op)]
            return operator(self._eval_node(node.operand, values))
        if isinstance(node, ast.Call):
            function = _ALLOWED_FUNCTIONS[node.func.id]
            arguments = [self._eval_node(arg, values) for arg in node.args]
            return function(*arguments)
        raise ValueError(f"Nodo no evaluable: {type(node).__name__}")
