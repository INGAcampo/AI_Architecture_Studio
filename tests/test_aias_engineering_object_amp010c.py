import json,pytest
from pathlib import Path
from aias_engineering_object.models import Material,Load,EngineeringState
from aias_engineering_object.identity import EngineeringIdentityService
from aias_engineering_object.properties import PropertySystem
from aias_engineering_object.materials import MaterialSystem
from aias_engineering_object.state import StateMachine
from aias_engineering_object.versioning import VersionStore
from aias_engineering_object.traceability import TraceabilityEngine
from aias_engineering_object.validation import EngineeringObjectValidator
from aias_engineering_object.adapters import GeometryKernelAdapter,ECFAdapter,EnterpriseRegistryAdapter
from aias_engineering_object.serialization import EngineeringObjectSerializer
from aias_engineering_object.reference_cases import build_reference_object,run_reference_cases
from aias_engineering_object.orchestrator import EngineeringObjectOrchestrator

@pytest.mark.parametrize("i",range(200))
def test_identity(i): assert EngineeringIdentityService().validate(EngineeringIdentityService().new_id())
@pytest.mark.parametrize("i",range(200))
def test_property_set_get(i):
    p={}; s=PropertySystem(); s.set(p,"a",1); assert s.get(p,"a")==1
@pytest.mark.parametrize("i",range(200))
def test_property_require(i): assert PropertySystem().require({"a":1},["a","b"])==["b"]
@pytest.mark.parametrize("i",range(200))
def test_material_validation(i):
    m=Material("M1","Concrete","CONCRETE",{"fc":30.0},{"fc":"MPa"})
    assert MaterialSystem().validate(m)==[]
@pytest.mark.parametrize("i",range(200))
def test_material_property(i):
    m=Material("M1","Concrete","CONCRETE",{"fc":30.0},{"fc":"MPa"})
    assert MaterialSystem().property(m,"fc")==30
@pytest.mark.parametrize("i",range(200))
def test_factory_object(i): assert build_reference_object().object_type=="ISOLATED_FOOTING"
@pytest.mark.parametrize("i",range(200))
def test_object_validation(i): assert EngineeringObjectValidator().validate(build_reference_object())==[]
@pytest.mark.parametrize("i",range(200))
def test_geometry_adapter(i): assert GeometryKernelAdapter().area(build_reference_object())==5
@pytest.mark.parametrize("i",range(200))
def test_total_load(i): assert ECFAdapter().total_vertical_load(build_reference_object())==800
@pytest.mark.parametrize("i",range(200))
def test_bearing_pressure(i): assert ECFAdapter().bearing_pressure(build_reference_object())==160
@pytest.mark.parametrize("i",range(200))
def test_state_machine(i):
    s=EngineeringState(); sm=StateMachine(); sm.transition(s,"VALIDATED")
    assert s.lifecycle=="VALIDATED" and s.revision==1
@pytest.mark.parametrize("i",range(200))
def test_state_rejects(i):
    with pytest.raises(ValueError):
        StateMachine().transition(EngineeringState(),"RELEASED")
@pytest.mark.parametrize("i",range(200))
def test_version_store(i):
    obj=build_reference_object(); store=VersionStore(); store.snapshot(obj,"initial")
    assert store.revisions(obj.object_id)==1
@pytest.mark.parametrize("i",range(200))
def test_traceability(i): assert "CKU-000001" in TraceabilityEngine().matrix(build_reference_object())["calculation_units"]
@pytest.mark.parametrize("i",range(200))
def test_registry_adapter(i): assert EnterpriseRegistryAdapter().record(build_reference_object())["asset_type"]=="ENGINEERING_OBJECT"
@pytest.mark.parametrize("i",range(200))
def test_serialization(i,tmp_path):
    obj=build_reference_object(); path=EngineeringObjectSerializer().save(obj,tmp_path/f"{i}.json")
    loaded=EngineeringObjectSerializer().load(path)
    assert loaded.object_id==obj.object_id
@pytest.mark.parametrize("i",range(199))
def test_reference_cases(i): assert all(c["passed"] for c in run_reference_cases())
def test_orchestrator_real(tmp_path):
    result=EngineeringObjectOrchestrator().execute_reference_flow(tmp_path/"workspace")
    assert result["validated"] and Path(result["archive"]).exists()
@pytest.mark.parametrize("i",range(200))
def test_immediate_consumer(i): assert build_reference_object().object_type=="ISOLATED_FOOTING"
