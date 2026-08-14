from aias_professional_qa import ProfessionalQAGate
def test_blocked_overrides_score():
 r=ProfessionalQAGate().evaluate([('BIM','PRODUCTION_READY','a','Graph',''),('DWG','BLOCKED','b','CAD','Install native DWG writer'),('Steel','PRELIMINARY','c','Standards','Verify detailing rules')]); assert r['verdict']=='NOT_READY' and any(x['severity']=='CRITICAL' for x in r['findings'])
def test_ready_without_gaps():
 assert ProfessionalQAGate().evaluate([('BIM','PRODUCTION_READY','a','Graph',''),('Steel','DETAIL_READY','b','Design','')])['verdict']=='READY_FOR_EXECUTIVE_REISSUANCE'
