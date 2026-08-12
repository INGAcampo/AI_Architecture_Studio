import pytest
from engines.structural.collaboration import *

@pytest.mark.parametrize("index", range(120))
def test_collaboration(index):
    manager = BimCollaborationManager()
    discipline = list(Discipline)[index % len(Discipline)]
    model = FederatedModel(f"M{index}", f"Model {index}", discipline, index)
    manager.register(model)
    assert manager.latest_revision() == index
    assert manager.by_discipline(discipline) == (model,)
