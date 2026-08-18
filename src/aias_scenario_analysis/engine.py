from __future__ import annotations
import hashlib, json

class ScenarioAnalysisEngine:
    """Fail-closed scenario deltas; never substitutes an authenticated baseline."""
    allowed={"bearing_capacity_factor","groundwater_delta_m","seismic_demand_factor","rainfall_factor","differential_settlement_mm","structural_system"}
    def evaluate(self, baseline: dict, scenario: dict) -> dict:
        mode=baseline.get('mode')
        if mode not in {'REAL_PROJECT','PILOT_SYNTHETIC'}: raise ValueError('baseline mode required')
        if mode=='REAL_PROJECT' and not baseline.get('authenticated_provenance_sha256'): raise ValueError('real baseline requires authenticated provenance')
        if mode=='PILOT_SYNTHETIC' and not (baseline.get('SYNTHETIC_TEST_DATA') and baseline.get('NOT_FOR_CONSTRUCTION')): raise ValueError('synthetic isolation flags required')
        delta=scenario.get('delta',{}); unknown=set(delta)-self.allowed
        if unknown: raise ValueError('unsupported scenario inputs: '+','.join(sorted(unknown)))
        payload={'baseline_id':baseline['project_id'],'baseline_mode':mode,'scenario_id':scenario['scenario_id'],'delta':delta,'SYNTHETIC_TEST_DATA':mode=='PILOT_SYNTHETIC','NOT_FOR_CONSTRUCTION':mode=='PILOT_SYNTHETIC','requires_regeneration':['standards','analysis','foundation','reinforcement','drawings','quantities','reports','qa_qc']}
        payload['sha256']=hashlib.sha256(json.dumps(payload,sort_keys=True).encode()).hexdigest()
        return payload
