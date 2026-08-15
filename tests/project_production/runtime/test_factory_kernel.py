import json
from aias_project_production.runtime import ProjectFactoryKernel
def manifest(i): return {'project_id':i,'project_name':i,'mode':'PILOT_SYNTHETIC','scenario_id':'NOMINAL_CASE_001','SYNTHETIC_TEST_DATA':True,'NOT_FOR_CONSTRUCTION':True,'building_program':{'levels':2,'width_m':10,'length_m':12,'storey_height_m':3}}
def test_isolated_queue_and_checkpoint(tmp_path):
 k=ProjectFactoryKernel(tmp_path); k.enqueue(manifest('P1')); k.enqueue(manifest('P2')); assert k.next()['project_id']=='P1'; k.checkpoint('P1','TARGET_REACHED','V8',['a']); assert k.next()['project_id']=='P2'; assert json.loads((tmp_path/'projects/P2/PROJECT_STATE.json').read_text())['status']=='QUEUED'
