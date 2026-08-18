import pytest
from design.steel.connection_optimizer import *
@pytest.mark.parametrize("i",range(120))
def test_optimizer(i):
    opts=(ConnectionOption("A",.8,100,.8,10),ConnectionOption("B",.9,90,.6,12))
    assert ConnectionOptimizer().optimize(opts).recommended_option_id in {"A","B"}
