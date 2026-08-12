from analysis.steel_stability.stability_unity import StabilityUnity
class StabilityPipeline:
    def run_demo(self):
        member_id='STAB-DEMO-001'; slenderness=6000/120
        result=StabilityUnity().evaluate(500000,950000,100000000,220000000,15000000,70000000)
        return member_id,slenderness,result
