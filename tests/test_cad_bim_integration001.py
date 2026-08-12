from pathlib import Path
import pytest
from aias_cad_bim_integration import BimElement,CadBimBridge,InterchangeModel
from aias_cad_bim_integration.reference import lighthouse_model
from aias_cad_bim_integration.serialization import read,write
from aias_drawing_framework import DrawingExporter,Sheet
def sheet():return Sheet("S-BIM","B-001","BIM PLAN",420,297,"0","LIGHTHOUSE-001","AIAS","REVIEWER")
def test_lighthouse_bim_projects_to_canonical_drawing_and_all_formats(tmp_path):
 drawing,result=CadBimBridge().to_drawing(lighthouse_model(),sheet());exports=DrawingExporter().export(drawing,tmp_path);assert len(result.mappings)==2 and not result.losses and set(exports["formats"])=={"json","svg","dxf","pdf"}
def test_unsupported_semantics_are_explicitly_disclosed():
 model=lighthouse_model();unknown=BimElement("HVAC-1","Duct","Duct",((1,1),(2,1),(2,2)),{},"LIGHTHOUSE");model=InterchangeModel(model.model_id,model.version,model.units,model.elements+(unknown,),model.provenance);_,result=CadBimBridge().to_drawing(model,sheet());assert result.losses==({"element_id":"HVAC-1","reason":"unsupported_element_type","element_type":"Duct"},)
def test_interchange_round_trip_and_integrity(tmp_path):
 path=tmp_path/"model.json";evidence=write(lighthouse_model(),path);restored=read(path,evidence["sha256"]);assert restored==lighthouse_model()
 path.write_text("{}")
 with pytest.raises(ValueError,match="integrity_failure"):read(path,evidence["sha256"])
def test_property_sync_is_allowlisted_and_requires_transaction():
 result=CadBimBridge().synchronize_properties(lighthouse_model(),{"WALL-001":{"mark":"W2","unsafe":"x"},"X":{"mark":"X"}},{"mark"});assert result["changes"]["WALL-001"]["after"]=={"mark":"W2"} and len(result["rejected"])==2 and result["requires_transaction_commit"]
def test_units_identity_and_provenance_are_mandatory():
 model=lighthouse_model()
 with pytest.raises(ValueError,match="invalid_interchange_model"):CadBimBridge().validate(InterchangeModel(model.model_id,model.version,"m",model.elements,model.provenance))
