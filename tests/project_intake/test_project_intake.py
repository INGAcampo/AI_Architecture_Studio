from aias_project_intake import ProjectIntake
def test_intake_accepts_isolated_synthetic_manifest():
 m={'project_id':'A','project_name':'A','mode':'PILOT_SYNTHETIC','scenario_id':'NOMINAL_CASE_001','SYNTHETIC_TEST_DATA':True,'NOT_FOR_CONSTRUCTION':True,'building_program':{'levels':2,'width_m':10,'length_m':12,'storey_height_m':3}}
 assert len(ProjectIntake().validate(m)['sha256'])==64
def test_intake_fails_closed_on_missing_geometry():
 try: ProjectIntake().validate({'project_id':'A','project_name':'A','mode':'PILOT_SYNTHETIC','scenario_id':'N','building_program':{}})
 except ValueError:return
 raise AssertionError('invalid intake accepted')
