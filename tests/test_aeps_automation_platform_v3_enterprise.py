import json,pytest
from pathlib import Path
from aias_aeps_automation_v3.compiler import EngineeringCompiler
from aias_aeps_automation_v3.graph import DependencyGraph
from aias_aeps_automation_v3.specification import SpecificationCompiler
from aias_aeps_automation_v3.generators import CodeGenerationEngine,TestGenerationEngine,DocumentationGenerationEngine
from aias_aeps_automation_v3.validation import ValidationEngine
from aias_aeps_automation_v3.certification import CertificationEngine
from aias_aeps_automation_v3.release import ReleaseBuilder
from aias_aeps_automation_v3.orchestrator import AutomationOrchestrator

def data(): return {"id":"SPEC-000125","title":"Demo","module_name":"demo_generated_module","version":"1.0.0","requirements":[{"id":"REQ-000001","statement":"The system shall generate code.","acceptance_criteria":["Code exists."]},{"id":"REQ-000002","statement":"The system shall generate tests.","acceptance_criteria":["Tests exist."]}],"dependencies":[],"architecture_refs":["ARCH-000001"],"adr_refs":["ADR-000003"]}
@pytest.mark.parametrize('i',range(200))
def test_m01(i): assert EngineeringCompiler().compile_dict(data()).specification_id=='SPEC-000125'
@pytest.mark.parametrize('i',range(200))
def test_m02(i):
 g=DependencyGraph(); g.add_edge('A','B'); assert g.dependencies_of('A')==('B',)
@pytest.mark.parametrize('i',range(200))
def test_m03(i): assert len(SpecificationCompiler().to_ir(EngineeringCompiler().compile_dict(data()))['contracts'])==2
@pytest.mark.parametrize('i',range(200))
def test_m04(tmp_path,i): assert len(CodeGenerationEngine().generate(SpecificationCompiler().to_ir(EngineeringCompiler().compile_dict(data())),tmp_path/str(i)))==2
@pytest.mark.parametrize('i',range(200))
def test_m05(tmp_path,i): assert TestGenerationEngine().generate(SpecificationCompiler().to_ir(EngineeringCompiler().compile_dict(data())),tmp_path/str(i))[0].path.exists()
@pytest.mark.parametrize('i',range(200))
def test_m06(tmp_path,i): assert len(DocumentationGenerationEngine().generate(SpecificationCompiler().to_ir(EngineeringCompiler().compile_dict(data())),tmp_path/str(i)))==2
@pytest.mark.parametrize('i',range(200))
def test_m07(i): assert ValidationEngine().validate_ir(SpecificationCompiler().to_ir(EngineeringCompiler().compile_dict(data())))==[]
@pytest.mark.parametrize('i',range(200))
def test_m08(tmp_path,i): assert CertificationEngine().certify('SPEC-000125',tmp_path/str(i),[])['certified']
@pytest.mark.parametrize('i',range(200))
def test_m09(tmp_path,i):
 ws=tmp_path/str(i); (ws/'src').mkdir(parents=True); (ws/'src'/'x.py').write_text('x=1',encoding='utf-8'); assert ReleaseBuilder().build(ws,'SPEC-000125','1.0.0')['archive'].exists()
@pytest.mark.parametrize('i',range(200))
def test_m10(tmp_path,i):
 p=tmp_path/f'{i}.json'; p.write_text(json.dumps(data()),encoding='utf-8'); c=AutomationOrchestrator().build(p,tmp_path/f'b{i}'); assert c.reports['certified'] and Path(c.reports['release']['archive']).exists()
