import pytest
from engines.structural.results import *

@pytest.mark.parametrize("index", range(120))
def test_result_store(index):
    store = StructuralResultStore()
    kind = list(ResultKind)[index % len(ResultKind)]
    result = StructuralResult(f"R{index}", "C1", f"O{index%7}", kind, (float(index), float(index+1)))
    store.add(result)
    assert len(store.for_case("C1")) == 1
    assert len(store.for_object(result.object_id)) == 1
