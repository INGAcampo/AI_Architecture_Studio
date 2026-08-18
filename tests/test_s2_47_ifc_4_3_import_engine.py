import json
import pytest
from engines.structural.ifc_import import *

@pytest.mark.parametrize("index", range(120))
def test_ifc_import(index):
    engine = Ifc43ImportEngine()
    payload = json.dumps({
        "schema": "IFC4X3",
        "entities": [{
            "global_id": f"G{index}",
            "entity_type": "IfcWall" if index % 2 == 0 else "IfcBeam",
            "name": f"Object {index}",
            "properties": {"Index": index},
            "parent_id": None,
        }],
    })
    entities = engine.import_json(payload)
    assert len(entities) == 1
    assert entities[0].properties["Index"] == index
    assert len(engine.spatial_roots(entities)) == 1
