import pytest
from engines.ai.family_library import *
@pytest.mark.parametrize("i",range(120))
def test_library(i):
    m=FamilyLibraryManager();m.add(LibraryItem(f"door{i}","doors",1,{"width":0.9}))
    assert m.get(f"door{i}").payload["width"]==0.9
    assert m.by_category("doors")[0].item_id==f"door{i}"
    assert m.export_index()[f"door{i}"]["version"]==1
