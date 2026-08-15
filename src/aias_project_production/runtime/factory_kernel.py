from __future__ import annotations
import hashlib, json, time
from pathlib import Path
from aias_project_intake import ProjectIntake

TERMINAL={'TARGET_REACHED','WAITING_EXTERNAL_INPUT','DESIGN_REVISION_REQUIRED','TECHNICAL_BLOCKER'}

class ProjectFactoryKernel:
    """Single-writer project runtime: queue, isolated evidence and durable checkpoints."""
    def __init__(self, root):
        self.root=Path(root); self.projects=self.root/'projects'; self.projects.mkdir(parents=True,exist_ok=True); self.queue_path=self.root/'PROJECT_QUEUE.json'
    def enqueue(self, manifest):
        intake=ProjectIntake().validate(manifest); project=self.projects/manifest['project_id']
        if project.exists(): raise ValueError('project_id already exists')
        project.mkdir(); (project/'artifacts').mkdir(); (project/'logs').mkdir(); (project/'qa').mkdir(); (project/'manifests').mkdir()
        self._write(project/'PROJECT_MANIFEST.json',manifest); self._write(project/'PROJECT_DEPENDENCY_GRAPH.json',{'project_id':manifest['project_id'],'nodes':['intake','graph','analysis','drawings','quantities','reports','qa','manifest'],'edges':[{'from':'intake','to':'graph'},{'from':'graph','to':'analysis'},{'from':'analysis','to':'drawings'},{'from':'analysis','to':'quantities'},{'from':'drawings','to':'reports'},{'from':'quantities','to':'reports'},{'from':'reports','to':'qa'}]})
        self._state(project,{'status':'QUEUED','project_id':manifest['project_id'],'mode':manifest['mode'],'intake_sha256':intake['sha256'],'completed_gates':[],'artifacts':[],'blockers':[]})
        queue=self._queue(); queue.append({'project_id':manifest['project_id'],'status':'QUEUED'}); self._write(self.queue_path,queue); self._event(project,'QUEUED')
    def next(self):
        return next((x for x in self._queue() if x['status']=='QUEUED'),None)
    def manifest(self, project_id):
        """Return the immutable intake document for one isolated project."""
        return json.loads((self.projects/project_id/'PROJECT_MANIFEST.json').read_text(encoding='utf-8'))
    def state(self, project_id):
        return json.loads((self.projects/project_id/'PROJECT_STATE.json').read_text(encoding='utf-8'))
    def artifact_root(self, project_id):
        return self.projects/project_id/'artifacts'
    def mark_running(self, project_id):
        state=self.state(project_id)
        if state['status'] in TERMINAL:
            return state
        state.update(status='RUNNING',updated_at=time.time())
        self._state(self.projects/project_id,state)
        queue=self._queue(); [x.update(status='RUNNING') for x in queue if x['project_id']==project_id]; self._write(self.queue_path,queue)
        self._event(self.projects/project_id,'RUNNING')
        return state
    def checkpoint(self, project_id, status, gate, artifacts=(), blockers=()):
        project=self.projects/project_id; state=json.loads((project/'PROJECT_STATE.json').read_text())
        completed=list(dict.fromkeys(state['completed_gates']+[gate]))
        state.update(status=status,last_gate=gate,completed_gates=completed,artifacts=list(artifacts),blockers=list(blockers),updated_at=time.time()); self._state(project,state)
        queue=self._queue(); [x.update(status=status) for x in queue if x['project_id']==project_id]; self._write(self.queue_path,queue); self._event(project,status,gate=gate)
    def _queue(self): return json.loads(self.queue_path.read_text()) if self.queue_path.exists() else []
    def _state(self,p,v): self._write(p/'PROJECT_STATE.json',v)
    def _event(self,p,event,**extra):
        extra.update(event=event,timestamp=time.time()); (p/'logs'/'PROJECT_EXECUTION_JOURNAL.jsonl').open('a').write(json.dumps(extra,sort_keys=True)+'\n')
    @staticmethod
    def _write(path,value): path.write_text(json.dumps(value,indent=2,sort_keys=True),encoding='utf-8')
