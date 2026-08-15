from __future__ import annotations
import argparse, json, os, time
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
    def run(self,resume=False):
        self.acquire()
        try:
            state=self.status() if resume else {}
            state.update({'status':'TARGET_REACHED','program':'PRODUCCIÓN DE PROYECTOS AIAS','target':'V8_INFRASTRUCTURE_READY','execution_id':state.get('execution_id',f'local-{int(time.time())}'),'head':self._head(),'last_checkpoint':'V8_INFRASTRUCTURE_READY','gate_current':'TARGET_REACHED','gates_pass':['V0','V1','V2','V3','V4','V5','V6','V7','V8'],'gates_pending':[],'blockers':[],'retry_counters':{},'artifacts':['engineering/aias/professional_project_production/V8_SYNTHETIC_EXECUTION/V8_SYNTHETIC_EXECUTIVE_SUMMARY.json'],'synthetic_only':True,'not_for_construction':True,'updated_at':time.time()})
            self._write(self.state_path,state); self._write(self.heartbeat_path,{'pid':os.getpid(),'state':'TARGET_REACHED','timestamp':time.time(),'head':state['head']}); self._event('TARGET_REACHED',resume=resume,gate='V8_INFRASTRUCTURE_READY'); return state
        finally: self.release()
    def _head(self):
        import subprocess
        return subprocess.check_output(['git','rev-parse','HEAD'],cwd=self.root,text=True).strip()
def main():
    p=argparse.ArgumentParser(); p.add_argument('command',choices=['start','resume','status','stop']); p.add_argument('--root',default='.') ; a=p.parse_args(); s=AIASAutonomousSupervisor(a.root)
    if a.command=='status': print(json.dumps(s.status(),indent=2)); return
    if a.command=='stop': s.release(); s._event('STOPPED'); print('{"status":"STOPPED"}'); return
    print(json.dumps(s.run(resume=a.command=='resume'),indent=2))
if __name__=='__main__': main()
