import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.hpc.hpc_report import HPCReportEngine
    assert 'Parallel FEM Solver Report' in HPCReportEngine().build(4,2,1e-9,3,.75).markdown
