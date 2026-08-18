from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class OcctRuntimeInfo:
    available: bool
    binding: str
    version: str | None


class OcctRuntimeBackend:
    """Lazy OCP-backed geometry runtime for AIAS Wave 2.

    Importing this module does not require OCP. Runtime operations fail closed
    with RuntimeError when the validated dependency is not available.
    """

    @staticmethod
    def discover() -> OcctRuntimeInfo:
        try:
            import OCP
        except Exception:
            return OcctRuntimeInfo(False, "OCP", None)
        return OcctRuntimeInfo(True, "OCP", getattr(OCP, "__version__", None))

    @staticmethod
    def _require() -> Any:
        try:
            import OCP
        except Exception as exc:
            raise RuntimeError("OCP runtime is not available") from exc
        return OCP

    def make_box(self, dx: float, dy: float, dz: float):
        self._require()
        from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox

        if dx <= 0 or dy <= 0 or dz <= 0:
            raise ValueError("box dimensions must be positive")
        shape = BRepPrimAPI_MakeBox(float(dx), float(dy), float(dz)).Shape()
        if shape.IsNull():
            raise RuntimeError("OCCT returned a null box shape")
        return shape

    def fuse(self, left, right):
        self._require()
        from OCP.BRepAlgoAPI import BRepAlgoAPI_Fuse

        shape = BRepAlgoAPI_Fuse(left, right).Shape()
        if shape.IsNull():
            raise RuntimeError("OCCT fuse returned a null shape")
        return shape

    def cut(self, left, right):
        self._require()
        from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut

        shape = BRepAlgoAPI_Cut(left, right).Shape()
        if shape.IsNull():
            raise RuntimeError("OCCT cut returned a null shape")
        return shape

    def common(self, left, right):
        self._require()
        from OCP.BRepAlgoAPI import BRepAlgoAPI_Common

        shape = BRepAlgoAPI_Common(left, right).Shape()
        if shape.IsNull():
            raise RuntimeError("OCCT common returned a null shape")
        return shape

    def mesh(self, shape, linear_deflection: float = 0.5):
        self._require()
        from OCP.BRepMesh import BRepMesh_IncrementalMesh

        if linear_deflection <= 0:
            raise ValueError("linear_deflection must be positive")
        mesher = BRepMesh_IncrementalMesh(shape, float(linear_deflection))
        mesher.Perform()
        return shape
