import pytest
@pytest.mark.parametrize('i',range(120))
def test_module(i):
    from analysis.steel_library.steel_library_vertical_slice import SteelLibraryVerticalSlice
    r=SteelLibraryVerticalSlice().run()
    assert r.validation.valid and 'W14X38' in r.report
