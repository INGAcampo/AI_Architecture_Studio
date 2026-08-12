import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.contact.contact_diagnostics import ContactDiagnosticsEngine
    assert not ContactDiagnosticsEngine().inspect(True,1e-6,.01).warnings
