import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.hpc.hpc_vertical_slice import HPCVerticalSlice
    r=HPCVerticalSlice().run(((4,0),(0,9)),(8,18),('E1','E2','E3','E4'),4)
    assert r.run.converged and '# Parallel FEM Solver Report' in r.report.markdown
