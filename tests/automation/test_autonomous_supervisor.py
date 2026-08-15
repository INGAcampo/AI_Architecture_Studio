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
