import json
import pytest
from engines.structural.ifc_export import *

@pytest.mark.parametrize("index", range(120))
def test_ifc_export(index):
    engine = Ifc43ExportEngine()
    entity = IfcExportEntity(
        f"G{index}",
        "IfcWall",
        f"Wall {index}",
        {"Pset_WallCommon": {"Reference": str(index)}},
        ("Concrete",),
    )
    data = json.loads(engine.export_json((entity,)))
    assert data["schema"] == "IFC4X3"
    assert data["entities"][0]["materials"] == ["Concrete"]
    assert "IFCWALL" in engine.export_step_subset((entity,))
