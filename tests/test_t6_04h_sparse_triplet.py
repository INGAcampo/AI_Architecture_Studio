import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.hpc.sparse_triplet import SparseTripletBuilder
    b=SparseTripletBuilder();b.add(0,0,1);b.add(0,0,2);assert b.compressed()==((0,0,3.0),)
