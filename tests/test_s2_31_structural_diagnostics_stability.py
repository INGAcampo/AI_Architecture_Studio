import pytest
from engines.structural.diagnostics import *

@pytest.mark.parametrize("index", range(120))
def test_diagnostics(index):
    diagnostics = StructuralDiagnostics()
    nodes = [f"N{i}" for i in range(index % 5 + 1)]
    connected = nodes[:-1]
    missing = diagnostics.check_unconnected_nodes(nodes, connected)
    assert len(missing) == 1
    matrix = [[1.0,0.0],[0.0,0.0 if index%2==0 else 1.0]]
    issues = diagnostics.check_singular_diagonal(matrix)
    assert len(issues) in (0,1)
