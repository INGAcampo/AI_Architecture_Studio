from aias_project_production.factory import ProjectProductionFactory
def test_factory_rejects_non_synthetic(tmp_path):
    try: ProjectProductionFactory(tmp_path).run([{'project_id':'R','mode':'REAL_PROJECT'}])
    except ValueError: return
    raise AssertionError('real project accepted without authenticated baseline')
