from pathlib import Path
import pytest
from aias_capability_factory import CapabilityBlueprint,CapabilityFactory,CapabilityRegistry
from aias_development_platform import DevelopmentPlatform
def blueprint():return CapabilityBlueprint("CAP-993801","Wall Schedule","BIM","1.0.0",({"id":"REQ-993801","statement":"Generate a wall schedule capability.","acceptance_criteria":["Module exists."]},),("ARCH-CAP-993801",),("ADR-CAP-993801",),"AIAS Engineering","APR-993801",metadata={"vertical_evidence":{"specification":"SPEC-993801","architecture":"ARCH-CAP-993801","implementation":"generated:wall_schedule","consumer":"reference:bim_workspace","tests":"tests/test_capability_factory001.py","documentation":"docs/CAPABILITY_FACTORY001.md","installer":"AIAS_CAPABILITY_FACTORY001_GOVERNED_FACTORY_INSTALLER","traceability":"engineering/capability_factory001/compliance/TRACEABILITY.json","reference_case":"CASE-WALL-SCHEDULE-001"}})
def runners():
 def run(s,w):
  w.mkdir(parents=True,exist_ok=True);z=w/"release.zip";z.write_bytes(b"release");return {"certified":True,"artifacts":[str(z)],"archive":str(z),"traceability":1.0}
 return {k:run for k in ("v3","v4","v5")}
def test_blueprint_requires_identity_approval_and_traceability():
 with pytest.raises(ValueError,match="identity"):CapabilityBlueprint("BAD","","","1",(),(),(),"","").validate()
def test_registry_enforces_sequential_evidence_gates(tmp_path):
 r=CapabilityRegistry(tmp_path/"registry.json");r.register(blueprint())
 with pytest.raises(ValueError,match="transition"):r.advance("CAP-993801","MATERIALIZED",{"development_result":{}})
 with pytest.raises(ValueError,match="approval_id"):r.advance("CAP-993801","APPROVED",{})
def test_factory_materializes_validates_releases_and_emits(tmp_path):
 events=[];registry=CapabilityRegistry(tmp_path/"registry.json");platform=DevelopmentPlatform(tmp_path/"production",runners());record=CapabilityFactory(registry,platform,tmp_path/"production",events.append).materialize(blueprint())
 assert record["state"]=="RELEASED" and len(record["history"])==5 and len(record["evidence"]["release"]["sha256"])==64 and events[0]["type"]=="capability.released"
 assert CapabilityRegistry(registry.path).data["capabilities"]["CAP-993801"]["state"]=="RELEASED"
def test_blueprint_identity_is_immutable(tmp_path):
 r=CapabilityRegistry(tmp_path/"r.json");r.register(blueprint());changed=CapabilityBlueprint("CAP-993801","Changed","BIM","1.0.0",blueprint().requirements,blueprint().architecture_refs,blueprint().adr_refs,"AIAS Engineering","APR-993801")
 with pytest.raises(ValueError,match="conflict"):r.register(changed)
def test_real_development_platform_produces_reference_capability(tmp_path):
 registry=CapabilityRegistry(tmp_path/"real_registry.json");platform=DevelopmentPlatform(tmp_path/"real_production");record=CapabilityFactory(registry,platform,tmp_path/"real_production").materialize(blueprint())
 assert record["state"]=="RELEASED" and Path(record["evidence"]["release"]["archive"]).is_file()
