from aias_scenario_analysis import ScenarioAnalysisEngine
def test_synthetic_scenario_is_isolated_and_traced():
 baseline={'project_id':'PILOT-BUILDING-001','mode':'PILOT_SYNTHETIC','SYNTHETIC_TEST_DATA':True,'NOT_FOR_CONSTRUCTION':True}
 result=ScenarioAnalysisEngine().evaluate(baseline,{'scenario_id':'LOW_BEARING_001','delta':{'bearing_capacity_factor':0.75}})
 assert result['NOT_FOR_CONSTRUCTION'] and 'foundation' in result['requires_regeneration']
def test_real_project_fails_closed_without_provenance():
 try: ScenarioAnalysisEngine().evaluate({'project_id':'REAL','mode':'REAL_PROJECT'},{'scenario_id':'X','delta':{}})
 except ValueError: return
 raise AssertionError('unauthenticated real baseline accepted')
