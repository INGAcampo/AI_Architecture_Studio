from aias_project_intake import ProjectIntake
def test_intake_accepts_isolated_synthetic_manifest():
 m={'project_id':'A','project_name':'A','mode':'PILOT_SYNTHETIC','scenario_id':'NOMINAL_CASE_001','SYNTHETIC_TEST_DATA':True,'NOT_FOR_CONSTRUCTION':True,'building_program':{'levels':2,'width_m':10,'length_m':12,'storey_height_m':3}}
 assert len(ProjectIntake().validate(m)['sha256'])==64
def test_intake_fails_closed_on_missing_geometry():
 try: ProjectIntake().validate({'project_id':'A','project_name':'A','mode':'PILOT_SYNTHETIC','scenario_id':'N','building_program':{}})
 except ValueError:return
 raise AssertionError('invalid intake accepted')

def test_parametric_builder_creates_isolated_graph():
 from aias_project_intake.builders import ParametricProjectGraphBuilder
 m={'project_id':'PARAM-001','project_name':'Param','mode':'PILOT_SYNTHETIC','scenario_id':'NOMINAL_CASE_001','SYNTHETIC_TEST_DATA':True,'NOT_FOR_CONSTRUCTION':True,'building_program':{'levels':3,'width_m':10,'length_m':12,'storey_height_m':3}}
 graph=ParametricProjectGraphBuilder().build(m); assert graph.project_id=='PARAM-001' and len([n for n in graph.nodes if n['type']=='level'])==3
 types=[n['type'] for n in graph.nodes]
 assert types.count('column')==12 and types.count('beam')==12 and types.count('foundation')==4
 assert {'grid','wall','door','window','roof'} <= set(types)
