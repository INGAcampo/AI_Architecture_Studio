from pathlib import Path
import json, subprocess, time
ROOT=Path(__file__).resolve().parents[1]
AUTO=Path(r'C:\Program Files\Autodesk\AutoCAD 2027\accoreconsole.exe')
DWG=ROOT/'engineering/aias/dependency_resolution/DR-01A_EXECUTIVE_DWG_CLOSURE/output/native/A-101.dwg'
OUT=ROOT/'engineering/aias/dependency_resolution/DR-01A_EXECUTIVE_DWG_CLOSURE/output/xdata_atomic'; OUT.mkdir(parents=True,exist_ok=True)
def p(x): return str(x.resolve()).replace('\\','/')
def run(step,expr):
 sentinel=OUT/(step+'.txt'); script=OUT/(step+'.scr'); sentinel.unlink(missing_ok=True)
 script.write_text(f'(setq f (open "{p(sentinel)}" "w"))\n{expr}\n(close f)\n(princ)\n_.QUIT\n',encoding='ascii')
 t=time.time(); q=subprocess.Popen([str(AUTO),'/i',str(DWG),'/s',str(script)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 try: o,e=q.communicate(timeout=30); timeout=False
 except subprocess.TimeoutExpired: q.kill(); o,e=q.communicate(); timeout=True
 return {'step':step,'pid':q.pid,'seconds':round(time.time()-t,3),'timeout':timeout,'exit':q.returncode,'sentinel':sentinel.exists(),'stdout_tail':o[-1000:],'stderr_tail':e[-1000:]}
steps=[
 ('STEP_01_OPEN','(write-line "OPEN" f)'),
 ('STEP_02_ENTITY_ITERATION','(setq e (entnext) n 0) (while e (setq n (+ n 1)) (setq e (entnext e))) (write-line (itoa n) f)'),
 ('STEP_03_HANDLE','(setq e (entnext) d (entget e)) (write-line (cdr (assoc 5 d)) f)'),
 ('STEP_04_APPID','(setq a (tblsearch "APPID" "AIAS")) (write-line (if a "AIAS_FOUND" "AIAS_MISSING") f)'),
 ('STEP_05_XDATA','(setq e (entnext) d (entget e (list "AIAS")) x (assoc -3 d)) (write-line (if x "XDATA_FOUND" "XDATA_MISSING") f)'),
 ('STEP_06_SERIALIZE','(setq e (entnext) d (entget e (list "AIAS")) x (cdr (assoc -3 d)) a (assoc "AIAS" x) i (cdr (assoc 1000 (cdr a)))) (write-line i f)'),
 ('STEP_07_EXIT','(write-line "EXIT_READY" f)')]
out=[]
for s,e in steps:
 r=run(s,e); out.append(r)
 if r['timeout'] or r['exit']!=0 or not r['sentinel']: break
(OUT/'DR01A_XDATA_ATOMIC.json').write_text(json.dumps(out,indent=2),encoding='utf-8'); print(json.dumps(out,indent=2))
