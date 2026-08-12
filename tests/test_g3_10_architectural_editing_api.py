import pytest
from bim_authoring.architectural_editing import *

@pytest.mark.parametrize("i", range(120))
def test_editing(i):
    api = ArchitecturalEditingAPI()
    api.add("A", {"value": 1})
    result = api.transaction((
        lambda store: ("A", {"value": 2}),
        lambda store: ("B", {"value": 3}),
    ))
    assert result.committed
    assert result.changed_ids == ("A", "B")
    assert api.get("A")["value"] == 2
    assert api.all_ids() == ("A", "B")
