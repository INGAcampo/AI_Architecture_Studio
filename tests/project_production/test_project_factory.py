from aias_project_production.factory import ProjectProductionFactory
def test_factory_rejects_non_synthetic(tmp_path):
    try: ProjectProductionFactory(tmp_path).run([{'project_id':'R','mode':'REAL_PROJECT'}])
    except ValueError: return
    raise AssertionError('real project accepted without authenticated baseline')

def test_factory_rejects_duplicate_project_ids(tmp_path):
    manifests=[{'project_id':'X','mode':'PILOT_SYNTHETIC','SYNTHETIC_TEST_DATA':True,'NOT_FOR_CONSTRUCTION':True}]*2
    try: ProjectProductionFactory(tmp_path).run(manifests)
    except ValueError as exc: assert 'duplicate' in str(exc); return
    raise AssertionError('duplicate project IDs accepted')
