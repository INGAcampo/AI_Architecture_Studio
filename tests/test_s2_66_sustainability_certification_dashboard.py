import pytest
from engines.structural.certification import *

@pytest.mark.parametrize("index", range(120))
def test_certification(index):
    credit = CertificationCredit(f"C{index}", 5 + index % 5, 10)
    score = CertificationDashboard().score((credit,))
    assert 0 <= score <= 100
