import pytest
from aias_adf2 import DependencyGraph, WorkPackage

def test_adf002_builds_safe_parallel_waves():
    graph = DependencyGraph((WorkPackage("root", "factory"), WorkPackage("geometry", "geometry", ("root",)), WorkPackage("bim", "bim", ("root",)), WorkPackage("merge", "integration", ("geometry", "bim"))))
    assert graph.plan().waves == (("root",), ("bim", "geometry"), ("merge",))

def test_adf002_rejects_cycles():
    graph = DependencyGraph((WorkPackage("a", "x", ("b",)), WorkPackage("b", "x", ("a",))))
    with pytest.raises(ValueError, match="dependency_cycle"): graph.plan()
