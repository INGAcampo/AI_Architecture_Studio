"""Multi-project synthetic factory over the certified V0-V8 orchestrator."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from .orchestrator import AIASProjectProductionOrchestrator
from aias_project_intake import ProjectIntake

class ProjectProductionFactory:
    def __init__(self, root): self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True)
    def run(self, manifests):
        results=[]
        manifest_ids=[x.get('project_id') for x in manifests]
        if len(manifest_ids)!=len(set(manifest_ids)): raise ValueError('duplicate project_id')
        seen=set()
        for manifest in manifests:
            self.validate_manifest(manifest); ProjectIntake().validate(manifest)
            project_id=manifest['project_id']
            if project_id in seen: raise ValueError('duplicate project_id')
            seen.add(project_id); out=self.root/project_id
            state=out/'PROJECT_AUTOMATION_STATE.json'; out.mkdir(parents=True,exist_ok=True)
            dependency={'project_id':project_id,'nodes':['intake','graph','V0','V1','V2','V3','V4','V5','V6','V7','V8','qa','manifest'],'mode':manifest['mode']}
            (out/'PROJECT_DEPENDENCY_GRAPH.json').write_text(json.dumps(dependency,indent=2),encoding='utf-8')
            state.write_text(json.dumps({'project_id':project_id,'status':'RUNNING','mode':manifest['mode']},indent=2),encoding='utf-8')
            result=AIASProjectProductionOrchestrator(out).run(manifest['scenario_id'], project_id=project_id, mode=manifest['mode'], project_name=manifest['project_name'], manifest=manifest)
            state.write_text(json.dumps({'project_id':project_id,'status':'TARGET_REACHED','mode':manifest['mode'],'checkpoint':'V8','artifacts':result['issuance']},indent=2,default=str),encoding='utf-8')
            result.update(project_id=project_id, mode='PILOT_SYNTHETIC', manifest_sha256=hashlib.sha256(json.dumps(manifest,sort_keys=True).encode()).hexdigest())
            results.append(result)
        ids=[x['project_id'] for x in results]
        payload={'schema':'aias.project_factory.v1','projects':results,'cross_project_contamination':len(ids)!=len(set(ids)),'verdict':'PROJECT_PRODUCTION_FACTORY_READY' if len(results)>=2 and not (len(ids)!=len(set(ids))) and all(x['V8']=='PASS' for x in results) else 'NOT_READY'}
        (self.root/'PROJECT_PRODUCTION_FACTORY_MANIFEST.json').write_text(json.dumps(payload,indent=2,default=str),encoding='utf-8')
        return payload

    @staticmethod
    def validate_manifest(manifest):
        required={'project_id','mode','project_name','scenario_id'}
        missing=required-set(manifest)
        if missing: raise ValueError('project manifest missing: '+','.join(sorted(missing)))
        if manifest['mode']=='PILOT_SYNTHETIC':
            if not manifest.get('SYNTHETIC_TEST_DATA') or not manifest.get('NOT_FOR_CONSTRUCTION'):
                raise ValueError('synthetic isolation flags required')
        elif manifest['mode']=='REAL_PROJECT':
            if not manifest.get('authenticated_provenance_sha256'):
                raise ValueError('real project requires authenticated provenance')
        else: raise ValueError('unsupported project mode')
