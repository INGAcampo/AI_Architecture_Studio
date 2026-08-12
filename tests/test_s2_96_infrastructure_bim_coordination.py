import pytest
from engines.civil.infrastructure_bim import *
@pytest.mark.parametrize("i",range(120))
def test_coordination(i):
    a=InfrastructureAsset(f"A{i}","civil",i);b=InfrastructureAsset(f"A{i}","civil",i+1);e=InfrastructureBimCoordinator()
    assert e.compare(a,b) is CoordinationStatus.WARNING
    assert e.latest((a,b)) is b
