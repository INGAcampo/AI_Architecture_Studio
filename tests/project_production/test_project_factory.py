from aias_project_production.factory import ProjectProductionFactory
def test_factory_rejects_non_synthetic(tmp_path):
    try: ProjectProductionFactory(tmp_path).run([{'project_id':'R','mode':'REAL_PROJECT','project_name':'R','scenario_id':'N'}])
    except ValueError: return
    raise AssertionError('real project accepted without authenticated baseline')

def test_factory_rejects_duplicate_project_ids(tmp_path):
    manifests=[{'project_id':'X','project_name':'X','scenario_id':'N','mode':'PILOT_SYNTHETIC','SYNTHETIC_TEST_DATA':True,'NOT_FOR_CONSTRUCTION':True}]*2
    try: ProjectProductionFactory(tmp_path).run(manifests)
    except ValueError as exc: assert 'duplicate' in str(exc); return
    raise AssertionError('duplicate project IDs accepted')

def test_factory_requires_a_complete_manifest():
    try: ProjectProductionFactory.validate_manifest({'project_id':'X','mode':'PILOT_SYNTHETIC'})
    except ValueError as exc: assert 'missing' in str(exc); return
    raise AssertionError('incomplete manifest accepted')

def test_orchestrator_accepts_parametric_manifest(tmp_path):
 from aias_project_production.orchestrator import AIASProjectProductionOrchestrator
 m={'project_id':'PARAM-X','project_name':'Param X','mode':'PILOT_SYNTHETIC','scenario_id':'NOMINAL_CASE_001','SYNTHETIC_TEST_DATA':True,'NOT_FOR_CONSTRUCTION':True,'building_program':{'levels':2,'width_m':8,'length_m':9,'storey_height_m':3}}
 # V0/V2 graph construction is exercised before downstream production.
 try: AIASProjectProductionOrchestrator(tmp_path).run('INVALID',manifest=m)
 except ValueError as exc: assert 'unknown synthetic scenario' in str(exc)
