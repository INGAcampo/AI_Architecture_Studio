import json
import pytest
from engines.structural.connectors import *

@pytest.mark.parametrize("index", range(120))
def test_connector(index):
    connector = SapEtabsConnector()
    model = ConnectorModel(
        f"Project {index}",
        ({"id":"N1","x":0,"y":0,"z":0},),
        ({"id":"M1","start":"N1","end":"N2"},),
        ({"id":"D","type":"dead"},),
    )
    target = ConnectorTarget.SAP2000 if index % 2 == 0 else ConnectorTarget.ETABS
    payload = connector.export_json(model, target)
    data = json.loads(payload)
    assert data["target"] == target.value
    restored = connector.import_json(payload)
    assert restored.project_name == model.project_name
