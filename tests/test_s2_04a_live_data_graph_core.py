from __future__ import annotations

import pytest

from engines.live_data_graph import (
    DependencyCycleError,
    DuplicateNodeError,
    LiveDataGraph,
    NodeNotFoundError,
    NodeState,
)


def _wall_graph() -> LiveDataGraph:
    graph = LiveDataGraph()
    graph.add_node("wall-01", "cad-object")
    graph.add_node("wall-01.geometry", "geometry")
    graph.add_node("wall-01.bim", "bim")
    graph.add_node("wall-01.renderer", "renderer")
    graph.add_dependency("wall-01", "wall-01.geometry")
    graph.add_dependency("wall-01.geometry", "wall-01.bim")
    graph.add_dependency("wall-01.geometry", "wall-01.renderer")
    return graph


def test_add_and_require_node_are_case_insensitive() -> None:
    graph = LiveDataGraph()
    node = graph.add_node("Wall-01", "cad-object", {"height": 3.0})

    assert graph.require_node("wall-01") is node
    assert "WALL-01" in graph


def test_duplicate_node_is_rejected_unless_replace_is_explicit() -> None:
    graph = LiveDataGraph()
    graph.add_node("wall-01", "cad-object")

    with pytest.raises(DuplicateNodeError):
        graph.add_node("WALL-01", "bim")

    replacement = graph.add_node("WALL-01", "bim", replace=True)
    assert replacement.kind == "bim"


def test_dependency_queries_return_deterministic_results() -> None:
    graph = _wall_graph()

    assert [n.node_id for n in graph.dependencies_of("wall-01.bim")] == [
        "wall-01.geometry"
    ]
    assert [n.node_id for n in graph.dependents_of("wall-01.geometry")] == [
        "wall-01.bim",
        "wall-01.renderer",
    ]


def test_recursive_dependents_follow_breadth_first_order() -> None:
    graph = _wall_graph()

    assert [
        n.node_id for n in graph.dependents_of("wall-01", recursive=True)
    ] == [
        "wall-01.geometry",
        "wall-01.bim",
        "wall-01.renderer",
    ]


def test_cycle_is_rejected_without_mutating_graph() -> None:
    graph = _wall_graph()

    with pytest.raises(DependencyCycleError):
        graph.add_dependency("wall-01.bim", "wall-01")

    assert graph.dependents_of("wall-01.bim") == ()


def test_mark_dirty_propagates_revision_to_affected_nodes() -> None:
    graph = _wall_graph()

    change = graph.mark_dirty("wall-01", reason="thickness_changed")

    assert change.affected_ids == (
        "wall-01",
        "wall-01.geometry",
        "wall-01.bim",
        "wall-01.renderer",
    )
    assert change.revision == 1
    assert all(node.state is NodeState.DIRTY for node in graph)
    assert all(node.revision == 1 for node in graph)


def test_unrelated_nodes_are_not_invalidated() -> None:
    graph = _wall_graph()
    graph.add_node("room-01", "space")

    graph.mark_dirty("wall-01.geometry")

    assert graph.require_node("room-01").state is NodeState.CLEAN


def test_update_payload_emits_immutable_change_to_listener() -> None:
    graph = LiveDataGraph()
    graph.add_node("wall-01", "cad-object")
    received = []
    unsubscribe = graph.subscribe(received.append)

    change = graph.update_payload(
        "wall-01",
        {"thickness": 0.25},
        metadata={"property": "Thickness"},
    )
    unsubscribe()
    graph.mark_dirty("wall-01")

    assert graph.require_node("wall-01").payload == {"thickness": 0.25}
    assert received == [change]
    assert change.metadata["property"] == "Thickness"
    with pytest.raises(TypeError):
        change.metadata["property"] = "Height"


def test_mark_clean_can_clear_entire_affected_branch() -> None:
    graph = _wall_graph()
    graph.mark_dirty("wall-01")

    graph.mark_clean("wall-01", recursive=True)

    assert all(node.state is NodeState.CLEAN for node in graph)


def test_remove_node_cleans_incoming_and_outgoing_dependencies() -> None:
    graph = _wall_graph()

    removed = graph.remove_node("wall-01.geometry")

    assert removed.node_id == "wall-01.geometry"
    assert graph.dependents_of("wall-01") == ()
    assert graph.dependencies_of("wall-01.bim") == ()


def test_missing_node_raises_domain_specific_error() -> None:
    graph = LiveDataGraph()

    with pytest.raises(NodeNotFoundError):
        graph.mark_dirty("missing")


def test_snapshot_contains_only_public_runtime_state() -> None:
    graph = LiveDataGraph()
    graph.add_node("wall-01", "cad-object", metadata={"category": "Walls"})

    assert graph.snapshot() == {
        "wall-01": {
            "kind": "cad-object",
            "state": "clean",
            "revision": 0,
            "metadata": {"category": "Walls"},
        }
    }
