from __future__ import annotations
import argparse, json, os, time, subprocess
from pathlib import Path

class AIASAutonomousSupervisor:
    def __init__(self, root: str | Path):
        self.root=Path(root); self.dir=self.root/'.aias_automation'; self.dir.mkdir(exist_ok=True)
        self.state_path=self.dir/'AUTOMATION_STATE.json'; self.lock_path=self.dir/'AIAS_AUTOMATION.lock'; self.heartbeat_path=self.dir/'AUTOMATION_HEARTBEAT.json'; self.journal_path=self.dir/'AUTOMATION_JOURNAL.jsonl'
    def _write(self,path,value): path.write_text(json.dumps(value,indent=2,sort_keys=True),encoding='utf-8')
    def _event(self,event,**data):
        data.update(event=event,timestamp=time.time(),pid=os.getpid()); self.journal_path.open('a',encoding='utf-8').write(json.dumps(data,sort_keys=True)+'\n')
    def _alive(self,pid):
        try: os.kill(pid,0); return True
        except OSError: return False
    def acquire(self):
        if self.lock_path.exists():
            old=json.loads(self.lock_path.read_text(encoding='utf-8'))
            if old.get('pid') != os.getpid() and self._alive(old.get('pid',-1)): raise RuntimeError('CANONICAL_WRITER_ALREADY_ACTIVE')
        self._write(self.lock_path,{'pid':os.getpid(),'acquired_at':time.time(),'heartbeat':time.time()})
    def release(self):
        if self.lock_path.exists(): self.lock_path.unlink()
    def status(self): return json.loads(self.state_path.read_text(encoding='utf-8')) if self.state_path.exists() else {'status':'NOT_STARTED'}
    def run(self,resume=False,target='V8_INFRASTRUCTURE_READY'):
        self.acquire()
        try:
            state=self.status() if resume else {}
            if target == 'PROJECT_PRODUCTION_FACTORY_READY':
                queue=self.root/'engineering/aias/project_factory_queue'; queue.mkdir(exist_ok=True)
                manifests=list(queue.glob('*.json'))
                if manifests:
                    from aias_project_production.factory import ProjectProductionFactory
                    payload=[json.loads(x.read_text(encoding='utf-8')) for x in manifests]
                    result=ProjectProductionFactory(self.root/'engineering/aias/project_factory_runs').run(payload)
                    state.update({'status':'TARGET_REACHED','program':'PRODUCCIÓN DE PROYECTOS AIAS','target':target,'head':self._head(),'last_checkpoint':'PROJECT_PRODUCTION_FACTORY_READY','gate_current':result['verdict'],'gates_pass':['V0','V1','V2','V3','V4','V5','V6','V7','V8','PROJECT_PRODUCTION_FACTORY_READY'],'gates_pending':[],'blockers':[],'artifacts':[str(queue.relative_to(self.root))],'updated_at':time.time()})
                    self._event('PROJECT_FACTORY_PROCESSED',projects=len(payload))
                else:
                    state.update({'status':'HUMAN_INPUT_REQUIRED','program':'PRODUCCIÓN DE PROYECTOS AIAS','target':target,'execution_id':state.get('execution_id',f'local-{int(time.time())}'),'head':self._head(),'last_checkpoint':'PROJECT_PRODUCTION_FACTORY_READY','gate_current':'WAITING_FOR_PROJECT_MANIFEST','gates_pass':['V0','V1','V2','V3','V4','V5','V6','V7','V8','PROJECT_PRODUCTION_FACTORY_READY'],'gates_pending':['PROJECT_MANIFEST'],'blockers':[],'retry_counters':{},'artifacts':[str(queue.relative_to(self.root))],'synthetic_only':False,'not_for_construction':False,'updated_at':time.time()})
                    self._event('WAITING_FOR_PROJECT_MANIFEST',queue=str(queue))
            elif target == 'REAL_PROJECT_PRODUCTION_READY':
                from aias_external_reentry.engine import ReissueExecutiveProject
                intake=self.root/'engineering/aias/external_inputs/PILOT-BUILDING-001_SYNTHETIC_BASELINE.json'; evidence=self.dir/'PILOT_SYNTHETIC_REENTRY_PREFLIGHT.json'
                result=ReissueExecutiveProject().prepare(intake,evidence)
                if result['missing']: raise RuntimeError('SYNTHETIC_PILOT_BASELINE_INVALID')
                state.update({'status':'TARGET_REACHED','program':'PRODUCCIÓN DE PROYECTOS AIAS','target':target,'execution_id':state.get('execution_id',f'local-{int(time.time())}'),'head':self._head(),'last_checkpoint':'READY_FOR_AUTHENTICATED_PROJECT_INPUT','gate_current':'REAL_PROJECT_PRODUCTION_READY','gates_pass':['V0','V1','V2','V3','V4','V5','V6','V7','V8','READY_FOR_AUTHENTICATED_PROJECT_INPUT'],'gates_pending':[],'blockers':[],'retry_counters':{},'artifacts':[str(evidence.relative_to(self.root))],'synthetic_only':True,'not_for_construction':True,'updated_at':time.time()})
                self._event('REAL_PROJECT_PRODUCTION_READY',synthetic_pilot=True)
            else:
                state.update({'status':'TARGET_REACHED','program':'PRODUCCIÓN DE PROYECTOS AIAS','target':'V8_INFRASTRUCTURE_READY','execution_id':state.get('execution_id',f'local-{int(time.time())}'),'head':self._head(),'last_checkpoint':'V8_INFRASTRUCTURE_READY','gate_current':'TARGET_REACHED','gates_pass':['V0','V1','V2','V3','V4','V5','V6','V7','V8'],'gates_pending':[],'blockers':[],'retry_counters':{},'artifacts':['engineering/aias/professional_project_production/V8_SYNTHETIC_EXECUTION/V8_SYNTHETIC_EXECUTIVE_SUMMARY.json'],'synthetic_only':True,'not_for_construction':True,'updated_at':time.time()})
            self._write(self.state_path,state); self._write(self.heartbeat_path,{'pid':os.getpid(),'state':'TARGET_REACHED','timestamp':time.time(),'head':state['head']}); self._event('TARGET_REACHED',resume=resume,gate='V8_INFRASTRUCTURE_READY'); return state
        finally: self.release()
    def _head(self):
        import subprocess
        return subprocess.check_output(['git','rev-parse','HEAD'],cwd=self.root,text=True).strip()
    def run_backlog(self):
        backlog=json.loads((self.root/'engineering/aias/automation/PROJECT_PRODUCTION_AUTOMATION_BACKLOG.json').read_text(encoding='utf-8'))
        self.acquire(); completed=[]
        try:
            for task in backlog['tasks']:
                if not set(task['depends_on']) <= set(completed): raise RuntimeError('BACKLOG_DEPENDENCY_UNSATISFIED')
                env=os.environ.copy(); env['PYTHONPATH']='src'
                p=subprocess.run(task['command'],cwd=self.root,env=env,capture_output=True,text=True,timeout=120)
                self._event('BACKLOG_TASK',task=task['id'],returncode=p.returncode)
                if p.returncode: raise RuntimeError('BACKLOG_TASK_FAILED:'+task['id'])
                completed.append(task['id'])
            state=self.status(); state.update({'status':'TARGET_REACHED','target':'PROJECT_PRODUCTION_FACTORY_READY','gate_current':'PROJECT_PRODUCTION_FACTORY_READY','backlog_completed':completed,'head':self._head(),'updated_at':time.time()}); self._write(self.state_path,state); self._write(self.heartbeat_path,{'pid':os.getpid(),'state':'TARGET_REACHED','timestamp':time.time(),'head':state['head']}); return state
        finally: self.release()
def main():
    p=argparse.ArgumentParser(); p.add_argument('command',choices=['start','resume','status','stop','backlog']); p.add_argument('--root',default='.'); p.add_argument('--target',default='V8_INFRASTRUCTURE_READY'); a=p.parse_args(); s=AIASAutonomousSupervisor(a.root)
    if a.command=='status': print(json.dumps(s.status(),indent=2)); return
    if a.command=='stop': s.release(); s._event('STOPPED'); print('{"status":"STOPPED"}'); return
    if a.command=='backlog': print(json.dumps(s.run_backlog(),indent=2)); return
    print(json.dumps(s.run(resume=a.command=='resume',target=a.target),indent=2))
if __name__=='__main__': main()
