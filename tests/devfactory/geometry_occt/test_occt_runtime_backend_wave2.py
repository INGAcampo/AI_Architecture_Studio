from __future__ import annotations

import pytest

from src.engines.geometry.occt.runtime_backend import OcctRuntimeBackend


def test_occt_runtime_is_available_in_validated_wave2_environment():
    info = OcctRuntimeBackend.discover()
    assert info.available is True
    assert info.binding == "OCP"


def test_occt_box_boolean_and_mesh_golden_path():
    backend = OcctRuntimeBackend()
    box1 = backend.make_box(10, 10, 10)

    from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
    from OCP.gp import gp_Pnt

    box2 = BRepPrimAPI_MakeBox(gp_Pnt(5, 5, 5), 10, 10, 10).Shape()

    assert not box1.IsNull()
    assert not backend.fuse(box1, box2).IsNull()
    assert not backend.cut(box1, box2).IsNull()
    assert not backend.common(box1, box2).IsNull()
    assert not backend.mesh(box1, 0.5).IsNull()


@pytest.mark.parametrize(
    "dims",
    [(0, 1, 1), (1, 0, 1), (1, 1, 0), (-1, 1, 1)],
)
def test_occt_box_rejects_non_positive_dimensions(dims):
    backend = OcctRuntimeBackend()
    with pytest.raises(ValueError):
        backend.make_box(*dims)
