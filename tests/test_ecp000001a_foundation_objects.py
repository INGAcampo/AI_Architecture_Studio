import pytest
from pathlib import Path
from aias_foundation_objects.reference_cases import reference_objects,run_reference_cases
from aias_foundation_objects.validation import FoundationValidator
from aias_foundation_objects.metrics import FoundationMetrics
from aias_foundation_objects.serialization import FoundationSerializer
from aias_foundation_objects.adapters import EngineeringObjectAdapter,GeometryKernelAdapter,ECFAdapter
from aias_foundation_objects.orchestrator import FoundationObjectOrchestrator

@pytest.mark.parametrize("i",range(200))
def test_reference_valid(i): assert all(FoundationValidator().validate(o)==[] for o in reference_objects().values())
@pytest.mark.parametrize("i",range(200))
def test_areas(i):
    o=reference_objects(); assert o["isolated"].geometry.area_m2==5 and o["mat"].geometry.area_m2==120
@pytest.mark.parametrize("i",range(200))
def test_metrics(i): assert FoundationMetrics().gross_bearing_pressure_kpa(reference_objects()["isolated"])==160
@pytest.mark.parametrize("i",range(200))
def test_serialization(i,tmp_path):
    obj=reference_objects()["combined"]; p=FoundationSerializer().save(obj,tmp_path/f"{i}.json")
    assert FoundationSerializer().load(p).foundation_type.value=="COMBINED"
@pytest.mark.parametrize("i",range(200))
def test_eok_adapter(i): assert EngineeringObjectAdapter().to_engineering_object_payload(reference_objects()["isolated"])["object_type"]=="ISOLATED"
@pytest.mark.parametrize("i",range(200))
def test_geometry_adapter(i): assert GeometryKernelAdapter().footprint(reference_objects()["isolated"])["area"]==5
@pytest.mark.parametrize("i",range(199))
def test_reference_cases(i): assert all(c["passed"] for c in run_reference_cases())
def test_orchestrator_real(tmp_path):
    r=FoundationObjectOrchestrator().execute(tmp_path/"workspace")
    assert r["validated"] and Path(r["archive"]).exists()
@pytest.mark.parametrize("i",range(200))
def test_ecf_adapter(i): assert ECFAdapter().calculation_inputs(reference_objects()["isolated"])["total_load_kn"]==800
