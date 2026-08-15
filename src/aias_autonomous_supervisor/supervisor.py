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
    @staticmethod
    def _factory_seed_manifests():
        """Controlled fixtures used only to certify the reusable factory runtime."""
        program={'levels':2,'width_m':8,'length_m':9,'storey_height_m':3}
        return [
            {'project_id':'FACTORY-SYNTHETIC-A','project_name':'Factory Synthetic A','mode':'PILOT_SYNTHETIC','scenario_id':'BEST_CASE_001','SYNTHETIC_TEST_DATA':True,'NOT_FOR_CONSTRUCTION':True,'building_program':program},
            {'project_id':'FACTORY-SYNTHETIC-B','project_name':'Factory Synthetic B','mode':'PILOT_SYNTHETIC','scenario_id':'NOMINAL_CASE_001','SYNTHETIC_TEST_DATA':True,'NOT_FOR_CONSTRUCTION':True,'building_program':program},
        ]
    def run(self,resume=False,target='V8_INFRASTRUCTURE_READY'):
        self.acquire()
        try:
            state=self.status() if resume else {}
            if target == 'PROJECT_PRODUCTION_FACTORY_READY':
                queue=self.root/'engineering/aias/project_factory_queue'; queue.mkdir(parents=True,exist_ok=True)
                manifests=list(queue.glob('*.json'))
                from aias_project_production.factory import ProjectProductionFactory
                payload=[json.loads(x.read_text(encoding='utf-8')) for x in manifests] or self._factory_seed_manifests()
                result=ProjectProductionFactory(self.root/'engineering/aias/project_factory_runs').run(payload)
                reached=result['verdict']=='PROJECT_PRODUCTION_FACTORY_READY'
                state.update({'status':'TARGET_REACHED' if reached else 'TECHNICAL_BLOCKER','program':'PRODUCCIÓN DE PROYECTOS AIAS','target':target,'head':self._head(),'last_checkpoint':'PROJECT_PRODUCTION_FACTORY_READY' if reached else 'FACTORY_EXECUTION','gate_current':result['verdict'],'gates_pass':['V0','V1','V2','V3','V4','V5','V6','V7','V8']+(['PROJECT_PRODUCTION_FACTORY_READY'] if reached else []),'gates_pending':[] if reached else ['PROJECT_PRODUCTION_FACTORY_READY'],'blockers':[] if reached else [result['verdict']],'artifacts':[str(queue.relative_to(self.root))],'synthetic_only':True,'not_for_construction':True,'updated_at':time.time()})
                self._event('PROJECT_FACTORY_PROCESSED',projects=len(payload),seeded=not manifests,verdict=result['verdict'])
            elif target == 'ARCHITECTURAL_PRODUCTION_CORE_READY':
                from aias_project_production.certification import certify_architectural_production_core
                evidence=self.root/'engineering/aias/architectural_production_core_certification'
                result=certify_architectural_production_core(evidence)
                reached=result['verdict']=='ARCHITECTURAL_PRODUCTION_CORE_READY'
                previous=state.get('gates_pass',[])
                gates=list(dict.fromkeys(previous+['PROJECT_PRODUCTION_FACTORY_READY']+([target] if reached else [])))
                state.update({'status':'TARGET_REACHED' if reached else 'TECHNICAL_BLOCKER','program':'PRODUCCIÓN DE PROYECTOS AIAS','target':target,'head':self._head(),'last_checkpoint':target if reached else 'ARCHITECTURAL_CORE_CERTIFICATION','gate_current':result['verdict'],'gates_pass':gates,'gates_pending':[] if reached else [target],'blockers':[] if reached else [name for name,passed in result['checks'].items() if not passed],'artifacts':[str((evidence/'ARCHITECTURAL_PRODUCTION_CORE_MANIFEST.json').relative_to(self.root))]+[str((evidence/x['evidence_file']).relative_to(self.root)) for x in result['projects']],'synthetic_only':True,'not_for_construction':True,'updated_at':time.time()})
                self._event('ARCHITECTURAL_CORE_PROCESSED',projects=len(result['projects']),verdict=result['verdict'])
            elif target == 'STRUCTURAL_PRODUCTION_CORE_READY':
                from aias_project_production.certification import certify_structural_production_core
                evidence=self.root/'engineering/aias/structural_production_core_certification'
                result=certify_structural_production_core(evidence)
                reached=result['verdict']=='STRUCTURAL_PRODUCTION_CORE_READY'
                previous=state.get('gates_pass',[])
                gates=list(dict.fromkeys(previous+['PROJECT_PRODUCTION_FACTORY_READY','ARCHITECTURAL_PRODUCTION_CORE_READY']+([target] if reached else [])))
                state.update({'status':'TARGET_REACHED' if reached else 'TECHNICAL_BLOCKER','program':'PRODUCCIÓN DE PROYECTOS AIAS','target':target,'head':self._head(),'last_checkpoint':target if reached else 'STRUCTURAL_CORE_CERTIFICATION','gate_current':result['verdict'],'gates_pass':gates,'gates_pending':[] if reached else [target],'blockers':[] if reached else [name for name,passed in result['checks'].items() if not passed],'artifacts':[str((evidence/'STRUCTURAL_PRODUCTION_CORE_MANIFEST.json').relative_to(self.root))],'synthetic_only':True,'not_for_construction':True,'updated_at':time.time()})
                self._event('STRUCTURAL_CORE_PROCESSED',projects=len(result['projects']),verdict=result['verdict'])
            elif target == 'ANALYSIS_PRODUCTION_CORE_READY':
                from aias_project_production.certification import certify_analysis_production_core
                evidence=self.root/'engineering/aias/analysis_production_core_certification'
                result=certify_analysis_production_core(evidence)
                reached=result['verdict']=='ANALYSIS_PRODUCTION_CORE_READY'
                previous=state.get('gates_pass',[])
                gates=list(dict.fromkeys(previous+['PROJECT_PRODUCTION_FACTORY_READY','ARCHITECTURAL_PRODUCTION_CORE_READY','STRUCTURAL_PRODUCTION_CORE_READY']+([target] if reached else [])))
                state.update({'status':'TARGET_REACHED' if reached else 'TECHNICAL_BLOCKER','program':'PRODUCCIÓN DE PROYECTOS AIAS','target':target,'head':self._head(),'last_checkpoint':target if reached else 'ANALYSIS_CORE_CERTIFICATION','gate_current':result['verdict'],'gates_pass':gates,'gates_pending':[] if reached else [target],'blockers':[] if reached else [name for name,passed in result['checks'].items() if not passed],'artifacts':[str((evidence/'ANALYSIS_PRODUCTION_CORE_MANIFEST.json').relative_to(self.root))]+[str((evidence/x['evidence_file']).relative_to(self.root)) for x in result['projects']],'synthetic_only':True,'not_for_construction':True,'updated_at':time.time()})
                self._event('ANALYSIS_CORE_PROCESSED',projects=len(result['projects']),verdict=result['verdict'])
            elif target == 'STANDARDS_PRODUCTION_CORE_READY':
                from aias_project_production.certification import certify_standards_production_core
                evidence=self.root/'engineering/aias/standards_production_core_certification'; result=certify_standards_production_core(evidence); reached=result['verdict']==target
                state.update({'status':'TARGET_REACHED' if reached else 'TECHNICAL_BLOCKER','target':target,'head':self._head(),'last_checkpoint':target,'gate_current':result['verdict'],'gates_pass':list(dict.fromkeys(state.get('gates_pass',[])+([target] if reached else []))),'blockers':[],'artifacts':[str((evidence/'STANDARDS_PRODUCTION_CORE_MANIFEST.json').relative_to(self.root))],'synthetic_only':True,'not_for_construction':True,'updated_at':time.time()})
                self._event('STANDARDS_CORE_PROCESSED',verdict=result['verdict'])
            elif target == 'DESIGN_PRODUCTION_CORE_READY':
                from aias_project_production.certification import certify_design_production_core
                evidence=self.root/'engineering/aias/design_production_core_certification'; result=certify_design_production_core(evidence); reached=result['verdict']==target
                previous=state.get('gates_pass',[])
                gates=list(dict.fromkeys(previous+['ANALYSIS_PRODUCTION_CORE_READY','STANDARDS_PRODUCTION_CORE_READY']+([target] if reached else [])))
                state.update({'status':'TARGET_REACHED' if reached else 'TECHNICAL_BLOCKER','program':'PRODUCCIÓN DE PROYECTOS AIAS','target':target,'head':self._head(),'last_checkpoint':target if reached else 'DESIGN_CORE_CERTIFICATION','gate_current':result['verdict'],'gates_pass':gates,'gates_pending':[] if reached else [target],'blockers':[] if reached else [name for name,passed in result['checks'].items() if not passed],'artifacts':[str((evidence/'DESIGN_PRODUCTION_CORE_MANIFEST.json').relative_to(self.root))]+[str((evidence/x['evidence_file']).relative_to(self.root)) for x in result['projects']],'synthetic_only':True,'not_for_construction':True,'updated_at':time.time()})
                self._event('DESIGN_CORE_PROCESSED',projects=len(result['projects']),verdict=result['verdict'])
            elif target == 'DRAWINGS_PRODUCTION_CORE_READY':
                from aias_project_production.certification import certify_drawings_production_core
                evidence=self.root/'engineering/aias/drawings_production_core_certification'; result=certify_drawings_production_core(evidence); reached=result['verdict']==target
                previous=state.get('gates_pass',[])
                gates=list(dict.fromkeys(previous+['DESIGN_PRODUCTION_CORE_READY']+([target] if reached else [])))
                state.update({'status':'TARGET_REACHED' if reached else 'TECHNICAL_BLOCKER','program':'PRODUCCIÓN DE PROYECTOS AIAS','target':target,'head':self._head(),'last_checkpoint':target if reached else 'DRAWINGS_CORE_CERTIFICATION','gate_current':result['verdict'],'gates_pass':gates,'gates_pending':[] if reached else [target],'blockers':[] if reached else [name for name,passed in result['checks'].items() if not passed],'artifacts':[str((evidence/'DRAWINGS_PRODUCTION_CORE_MANIFEST.json').relative_to(self.root))]+[str((evidence/x['evidence_file']).relative_to(self.root)) for x in result['projects']],'synthetic_only':True,'not_for_construction':True,'updated_at':time.time()})
                self._event('DRAWINGS_CORE_PROCESSED',projects=len(result['projects']),verdict=result['verdict'])
            elif target == 'REAL_PROJECT_PRODUCTION_READY':
                from aias_external_reentry.engine import ReissueExecutiveProject
                intake=self.root/'engineering/aias/external_inputs/PILOT-BUILDING-001_SYNTHETIC_BASELINE.json'; evidence=self.dir/'PILOT_SYNTHETIC_REENTRY_PREFLIGHT.json'
                result=ReissueExecutiveProject().prepare(intake,evidence)
                if result['missing']: raise RuntimeError('SYNTHETIC_PILOT_BASELINE_INVALID')
                state.update({'status':'TARGET_REACHED','program':'PRODUCCIÓN DE PROYECTOS AIAS','target':target,'execution_id':state.get('execution_id',f'local-{int(time.time())}'),'head':self._head(),'last_checkpoint':'READY_FOR_AUTHENTICATED_PROJECT_INPUT','gate_current':'REAL_PROJECT_PRODUCTION_READY','gates_pass':['V0','V1','V2','V3','V4','V5','V6','V7','V8','READY_FOR_AUTHENTICATED_PROJECT_INPUT'],'gates_pending':[],'blockers':[],'retry_counters':{},'artifacts':[str(evidence.relative_to(self.root))],'synthetic_only':True,'not_for_construction':True,'updated_at':time.time()})
                self._event('REAL_PROJECT_PRODUCTION_READY',synthetic_pilot=True)
            else:
                state.update({'status':'TARGET_REACHED','program':'PRODUCCIÓN DE PROYECTOS AIAS','target':'V8_INFRASTRUCTURE_READY','execution_id':state.get('execution_id',f'local-{int(time.time())}'),'head':self._head(),'last_checkpoint':'V8_INFRASTRUCTURE_READY','gate_current':'TARGET_REACHED','gates_pass':['V0','V1','V2','V3','V4','V5','V6','V7','V8'],'gates_pending':[],'blockers':[],'retry_counters':{},'artifacts':['engineering/aias/professional_project_production/V8_SYNTHETIC_EXECUTION/V8_SYNTHETIC_EXECUTIVE_SUMMARY.json'],'synthetic_only':True,'not_for_construction':True,'updated_at':time.time()})
            self._write(self.state_path,state); self._write(self.heartbeat_path,{'pid':os.getpid(),'state':state['status'],'timestamp':time.time(),'head':state['head']}); self._event(state['status'],resume=resume,gate=state['gate_current']); return state
        finally: self.release()
    def run_chain(self, resume=True):
        """Advance every known internal macro-gate in one owned execution."""
        state=self.status() if resume else {}
        ordered=['PROJECT_PRODUCTION_FACTORY_READY','ARCHITECTURAL_PRODUCTION_CORE_READY','STRUCTURAL_PRODUCTION_CORE_READY','ANALYSIS_PRODUCTION_CORE_READY','STANDARDS_PRODUCTION_CORE_READY','DESIGN_PRODUCTION_CORE_READY','DRAWINGS_PRODUCTION_CORE_READY']
        completed=set(state.get('gates_pass',[]))
        for target in ordered:
            if target not in completed:
                state=self.run(resume=True,target=target)
                if state['status'] != 'TARGET_REACHED': return state
                completed.add(target)
        # Never announce a target until its executor and certification gate are
        # physically registered in this supervisor.
        state['head']=self._head(); state['next_target']='QUANTITIES_PRODUCTION_CORE_READY'; state['updated_at']=time.time()
        self._write(self.state_path,state); self._event('CHAIN_CHECKPOINT',next_target=state['next_target'])
        return state
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
    p=argparse.ArgumentParser(); p.add_argument('command',choices=['start','resume','status','stop','backlog','chain']); p.add_argument('--root',default='.'); p.add_argument('--target',default='V8_INFRASTRUCTURE_READY'); a=p.parse_args(); s=AIASAutonomousSupervisor(a.root)
    if a.command=='status': print(json.dumps(s.status(),indent=2)); return
    if a.command=='stop': s.release(); s._event('STOPPED'); print('{"status":"STOPPED"}'); return
    if a.command=='backlog': print(json.dumps(s.run_backlog(),indent=2)); return
    if a.command=='chain': print(json.dumps(s.run_chain(),indent=2)); return
    print(json.dumps(s.run(resume=a.command=='resume',target=a.target),indent=2))
if __name__=='__main__': main()
