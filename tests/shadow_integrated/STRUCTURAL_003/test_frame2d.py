import math
from structural_platform_frame.frame2d import (
    FrameNode,
    FrameElement,
    FrameLoad,
    FrameModel,
    solve_frame_2d,
)


E = 200e9
A = 0.02
I = 8e-5


def test_cantilever_tip_load_matches_closed_form():
    length = 3.0
    load = -10000.0

    model = FrameModel(
        nodes=(
            FrameNode("A", 0.0, 0.0, True, True, True),
            FrameNode("B", length, 0.0),
        ),
        elements=(
            FrameElement("AB", "A", "B", A, I, E),
        ),
        loads=(
            FrameLoad("B", fy_n=load),
        ),
    )

    result = solve_frame_2d(model)
    expected_v = load * length**3 / (3 * E * I)
    expected_rz = load * length**2 / (2 * E * I)

    assert math.isclose(result.displacements["B"][1], expected_v, rel_tol=1e-10)
    assert math.isclose(result.displacements["B"][2], expected_rz, rel_tol=1e-10)
    assert math.isclose(result.reactions["A"][1], -load, rel_tol=1e-10)
    assert math.isclose(result.reactions["A"][2], -load * length, rel_tol=1e-10)


def test_axial_bar_behavior_is_preserved():
    length = 2.0
    load = 5000.0

    model = FrameModel(
        nodes=(
            FrameNode("A", 0.0, 0.0, True, True, True),
            FrameNode("B", length, 0.0, False, True, True),
        ),
        elements=(
            FrameElement("AB", "A", "B", A, I, E),
        ),
        loads=(
            FrameLoad("B", fx_n=load),
        ),
    )

    result = solve_frame_2d(model)
    expected_u = load * length / (A * E)

    assert math.isclose(result.displacements["B"][0], expected_u, rel_tol=1e-10)
    assert math.isclose(result.reactions["A"][0], -load, rel_tol=1e-10)


def test_unstable_frame_fails_closed():
    model = FrameModel(
        nodes=(
            FrameNode("A", 0.0, 0.0),
            FrameNode("B", 1.0, 0.0),
        ),
        elements=(
            FrameElement("AB", "A", "B", A, I, E),
        ),
    )

    failed = False
    try:
        solve_frame_2d(model)
    except ValueError as exc:
        failed = "singular" in str(exc)
    assert failed is True
