import pytest
@pytest.mark.parametrize('i', range(120))
def test_module(i):
    from analysis.steel_member_design.local_buckling_classification import LocalBucklingClassifier
    assert LocalBucklingClassifier().classify(8,10,20)=='compact'
