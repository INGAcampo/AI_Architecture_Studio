import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    import importlib
    assert importlib.import_module('analysis.steel_library.section_filter') is not None
