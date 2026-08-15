"""Multi-project synthetic factory over the certified V0-V8 orchestrator."""
from __future__ import annotations
import hashlib, json
from pathlib import Path
from .orchestrator import AIASProjectProductionOrchestrator
from aias_project_intake import ProjectIntake
from .runtime import ProjectFactoryKernel

class ProjectProductionFactory:
    """Durable, single-writer factory for isolated project production runs."""
    def __init__(self, root, orchestrator_type=AIASProjectProductionOrchestrator):
        self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True)
        self.kernel=ProjectFactoryKernel(self.root/'runtime')
        self.orchestrator_type=orchestrator_type
    def run(self, manifests):
        manifest_ids=[x.get('project_id') for x in manifests]
        if len(manifest_ids)!=len(set(manifest_ids)): raise ValueError('duplicate project_id')
        for manifest in manifests:
            self.validate_manifest(manifest); ProjectIntake().validate(manifest)
            project_id=manifest['project_id']
            if not (self.kernel.projects/project_id).exists(): self.kernel.enqueue(manifest)
            elif self.kernel.manifest(project_id) != manifest: raise ValueError('project_id already belongs to a different manifest')
        return self.resume()

    def resume(self):
        """Run only queued projects; completed projects remain immutable checkpoints."""
        results=[]
        while job:=self.kernel.next():
            project_id=job['project_id']; manifest=self.kernel.manifest(project_id)
            self.kernel.mark_running(project_id)
            output=self.kernel.artifact_root(project_id)
            try:
                result=self.orchestrator_type(output).run(manifest['scenario_id'], project_id=project_id, mode=manifest['mode'], project_name=manifest['project_name'], manifest=manifest)
            except Exception as exc:
                self.kernel.checkpoint(project_id,'TECHNICAL_BLOCKER','FACTORY_EXECUTION',blockers=[str(exc)])
                raise
            result.update(project_id=project_id, mode=manifest['mode'], manifest_sha256=hashlib.sha256(json.dumps(manifest,sort_keys=True).encode()).hexdigest())
            status='TARGET_REACHED' if result.get('V8')=='PASS' else 'DESIGN_REVISION_REQUIRED'
            self.kernel.checkpoint(project_id,status,'V8',artifacts=[result.get('issuance',{})],blockers=[] if status=='TARGET_REACHED' else [result.get('verdict','V8 failed')])
            results.append(result)
        return self._factory_manifest(results)

    def _factory_manifest(self, new_results):
        projects=[]
        for project in sorted(self.kernel.projects.iterdir()):
            if project.is_dir():
                state=self.kernel.state(project.name)
                projects.append({'project_id':project.name,'state':state,'artifact_root':str(self.kernel.artifact_root(project.name))})
        ids=[x['project_id'] for x in projects]
        ready=len(projects)>=2 and len(ids)==len(set(ids)) and all(x['state']['status']=='TARGET_REACHED' for x in projects)
        payload={'schema':'aias.project_factory.v2','projects':projects,'new_results':new_results,'cross_project_contamination':False,'isolation_verified':len({x['artifact_root'] for x in projects})==len(projects),'verdict':'PROJECT_PRODUCTION_FACTORY_READY' if ready else 'NOT_READY'}
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
