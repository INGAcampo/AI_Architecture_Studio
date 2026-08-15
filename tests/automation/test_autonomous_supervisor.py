from aias_autonomous_supervisor.supervisor import AIASAutonomousSupervisor
def test_resume_and_single_writer(tmp_path):
 s=AIASAutonomousSupervisor(tmp_path); s._head=lambda:'abc'; first=s.run(); assert first['gate_current']=='TARGET_REACHED'; second=s.run(resume=True); assert second['execution_id']==first['execution_id']; assert s.heartbeat_path.exists() and s.journal_path.exists()

def test_factory_target_seeds_two_isolated_synthetic_projects(tmp_path, monkeypatch):
    captured=[]
    class FakeFactory:
        def __init__(self, root): pass
        def run(self, manifests):
            captured.extend(manifests)
            return {'verdict':'PROJECT_PRODUCTION_FACTORY_READY'}
    import aias_project_production.factory
    monkeypatch.setattr(aias_project_production.factory, 'ProjectProductionFactory', FakeFactory)
    supervisor=AIASAutonomousSupervisor(tmp_path); supervisor._head=lambda:'abc'
    state=supervisor.run(target='PROJECT_PRODUCTION_FACTORY_READY')
    assert state['status']=='TARGET_REACHED'
    assert [x['project_id'] for x in captured]==['FACTORY-SYNTHETIC-A','FACTORY-SYNTHETIC-B']
    assert all(x['SYNTHETIC_TEST_DATA'] and x['NOT_FOR_CONSTRUCTION'] for x in captured)

def test_architectural_target_continues_from_factory_gate(tmp_path, monkeypatch):
    def fake_certify(output):
        return {
            'verdict':'ARCHITECTURAL_PRODUCTION_CORE_READY',
            'checks':{'two_projects':True},
            'projects':[
                {'evidence_file':'A.json'},
                {'evidence_file':'B.json'},
            ],
        }
    import aias_project_production.certification
    monkeypatch.setattr(
        aias_project_production.certification,
        'certify_architectural_production_core',
        fake_certify,
    )
    supervisor=AIASAutonomousSupervisor(tmp_path); supervisor._head=lambda:'abc'
    state=supervisor.run(target='ARCHITECTURAL_PRODUCTION_CORE_READY')
    assert state['status']=='TARGET_REACHED'
    assert state['gates_pass'][-2:]==[
        'PROJECT_PRODUCTION_FACTORY_READY',
        'ARCHITECTURAL_PRODUCTION_CORE_READY',
    ]

def test_chain_skips_certified_gates_and_starts_next_pending(monkeypatch, tmp_path):
    supervisor=AIASAutonomousSupervisor(tmp_path); supervisor._head=lambda:'abc'
    calls=[]
    def fake_run(resume=False,target=''):
        calls.append(target)
        return {'status':'TARGET_REACHED','gates_pass':[target], 'head':'abc'}
    monkeypatch.setattr(supervisor, 'run', fake_run)
    supervisor._write(supervisor.state_path, {'gates_pass':['PROJECT_PRODUCTION_FACTORY_READY']})
    state=supervisor.run_chain()
    assert calls==['ARCHITECTURAL_PRODUCTION_CORE_READY','STRUCTURAL_PRODUCTION_CORE_READY','ANALYSIS_PRODUCTION_CORE_READY','STANDARDS_PRODUCTION_CORE_READY','DESIGN_PRODUCTION_CORE_READY']
    assert state['next_target']=='DRAWINGS_PRODUCTION_CORE_READY'

def test_analysis_target_continues_from_structural_gate(tmp_path, monkeypatch):
    def fake_certify(output):
        return {
            'verdict':'ANALYSIS_PRODUCTION_CORE_READY',
            'checks':{'equilibrium_verified':True},
            'projects':[
                {'evidence_file':'A.json'},
                {'evidence_file':'B.json'},
            ],
        }
    import aias_project_production.certification
    monkeypatch.setattr(
        aias_project_production.certification,
        'certify_analysis_production_core',
        fake_certify,
    )
    supervisor=AIASAutonomousSupervisor(tmp_path); supervisor._head=lambda:'abc'
    state=supervisor.run(target='ANALYSIS_PRODUCTION_CORE_READY')
    assert state['status']=='TARGET_REACHED'
    assert state['gates_pass'][-2:]==[
        'STRUCTURAL_PRODUCTION_CORE_READY',
        'ANALYSIS_PRODUCTION_CORE_READY',
    ]

def test_design_target_continues_from_analysis_and_standards(tmp_path, monkeypatch):
    def fake_certify(output):
        return {
            'verdict':'DESIGN_PRODUCTION_CORE_READY',
            'checks':{'analysis_bound':True},
            'projects':[{'evidence_file':'A.json'},{'evidence_file':'B.json'}],
        }
    import aias_project_production.certification
    monkeypatch.setattr(
        aias_project_production.certification,
        'certify_design_production_core',
        fake_certify,
    )
    supervisor=AIASAutonomousSupervisor(tmp_path); supervisor._head=lambda:'abc'
    state=supervisor.run(target='DESIGN_PRODUCTION_CORE_READY')
    assert state['status']=='TARGET_REACHED'
    assert state['gates_pass'][-3:]==[
        'ANALYSIS_PRODUCTION_CORE_READY',
        'STANDARDS_PRODUCTION_CORE_READY',
        'DESIGN_PRODUCTION_CORE_READY',
    ]
