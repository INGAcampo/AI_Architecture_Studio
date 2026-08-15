"""Multi-project synthetic factory over the certified V0-V8 orchestrator."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from .orchestrator import AIASProjectProductionOrchestrator

class ProjectProductionFactory:
    def __init__(self, root): self.root=Path(root)
    def run(self, manifests):
        results=[]
        for manifest in manifests:
            if manifest.get('mode') != 'PILOT_SYNTHETIC' or not manifest.get('SYNTHETIC_TEST_DATA') or not manifest.get('NOT_FOR_CONSTRUCTION'):
                raise ValueError('factory accepts only explicit synthetic certification manifests')
            project_id=manifest['project_id']; out=self.root/project_id
            result=AIASProjectProductionOrchestrator(out).run('NOMINAL_CASE_001')
            result.update(project_id=project_id, mode='PILOT_SYNTHETIC', manifest_sha256=hashlib.sha256(json.dumps(manifest,sort_keys=True).encode()).hexdigest())
            results.append(result)
        payload={'schema':'aias.project_factory.v1','projects':results,'verdict':'PROJECT_PRODUCTION_FACTORY_READY' if all(x['V8']=='PASS' for x in results) else 'NOT_READY'}
        (self.root/'PROJECT_PRODUCTION_FACTORY_MANIFEST.json').write_text(json.dumps(payload,indent=2,default=str),encoding='utf-8')
        return payload
