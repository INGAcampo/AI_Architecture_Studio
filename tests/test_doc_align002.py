from pathlib import Path
from aias_documentation_program.planner import build_plan,write_plan
from aias_governance_assurance.documentation import audit
def test_risk_priority_prefers_engineering_criticality(tmp_path):
 for name in ('aias_low','aias_foundation_calcs'):
  p=tmp_path/'src'/name;p.mkdir(parents=True);(p/'x.py').write_text('def public():\n return 1\n',encoding='utf-8')
 assert build_plan(tmp_path)['priority_queue'][0]['package']=='aias_foundation_calcs'
def test_plan_is_persistent_evidence(tmp_path):
 p=tmp_path/'src'/'aias_demo';p.mkdir(parents=True);(p/'x.py').write_text('def public():\n return 1\n',encoding='utf-8');result=write_plan(tmp_path,tmp_path/'out'/'plan.json');assert result['total_debt']==2 and (tmp_path/'out'/'plan.json').exists()
def test_repository_has_zero_public_documentation_debt():
 root=Path(__file__).resolve().parents[1];result=audit(root);assert result['complete'],result['missing'][:20];assert result['modules']==result['documented_modules'];assert result['public_symbols']==result['documented_public_symbols']
