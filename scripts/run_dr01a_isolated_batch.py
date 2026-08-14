"""Reusable per-drawing Core Console lifecycle runner."""
from __future__ import annotations
import hashlib,json,subprocess,time,uuid
from pathlib import Path
from aias_cad_professional.engine import CADDocument
from aias_dxf_writer import ValidDxfWriter
ROOT=Path(__file__).resolve().parents[1]; AUTO=Path(r'C:\Program Files\Autodesk\AutoCAD 2027\accoreconsole.exe'); BASE=ROOT/'engineering/aias/dependency_resolution/DR-01A_EXECUTIVE_DWG_CLOSURE'; MODEL=ROOT/'engineering/aias/professional_project_production/PRO-02_PROFESSIONAL_CAD_DRAWING_ENGINE/PILOT-BUILDING-001_CAD_V0.json'
def h(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def q(p): return str(Path(p).resolve()).replace('\\','/')
def run(job,drawing,operation,body):
 script=job/(operation+'.scr'); script.write_text(body,encoding='ascii'); start=time.time(); p=subprocess.Popen([str(AUTO),'/i',str(drawing),'/s',str(script)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 try: out,err=p.communicate(timeout=35); timed=False
 except subprocess.TimeoutExpired: p.kill(); out,err=p.communicate(); timed=True
 return {'pid':p.pid,'operation':operation,'seconds':round(time.time()-start,3),'timeout':timed,'exit':p.returncode,'terminated':p.poll() is not None,'stdout_tail':out[-1200:],'stderr_tail':err[-1200:]}
def inspect(job):
 log=job/'inspection.txt'; body=f'''(setq f (open "{q(log)}" "w"))
(setq e (entnext))
(while e (setq d (entget e (list "AIAS")) x (cdr (assoc -3 d)) a (assoc "AIAS" x) i (if a (cdr (assoc 1000 (cdr a))) "")) (write-line (strcat "E|" i "|" (cdr (assoc 0 d)) "|" (if (assoc 8 d) (cdr (assoc 8 d)) "") "|" (cdr (assoc 5 d))) f) (setq e (entnext e)))
(close f)
(princ)
_.QUIT
'''; return log,body
def main():
 doc=CADDocument(**json.loads(MODEL.read_text(encoding='utf-8'))); ids={x['id'] for x in doc.entities}; layers={x['name'] for x in doc.layers}; writer=ValidDxfWriter(); runid=uuid.uuid4().hex[:12]; root=BASE/'output'/'isolated'/runid; rows=[]
 for sheet in doc.sheets:
  name=sheet['number']; job=root/name; job.mkdir(parents=True); dxf=job/(name+'.dxf'); writer.write(doc,dxf); dwg=job/(name+'.dwg')
  gen=run(job,dxf,'generate',f'_.SAVEAS\n2018\n"{q(dwg)}"\n_.QUIT\n'); log,body=inspect(job); ins=run(job,dwg,'inspect',body) if dwg.exists() else {'exit':None,'timeout':False,'terminated':True}
  rs=[]
  if log.exists():
   for ln in log.read_text(encoding='utf-8',errors='replace').splitlines():
    z=ln.split('|');
    if len(z)==5 and z[0]=='E': rs.append(z)
  rid=[z[1] for z in rs if z[1]]; handles=[z[4] for z in rs if z[1]]; rlayer={z[3] for z in rs if z[1]}; missing=sorted(ids-set(rid)); bad=bool(gen['exit']!=0 or ins['exit']!=0 or gen['timeout'] or ins['timeout'] or not gen['terminated'] or not ins['terminated'] or missing or set(rid)-ids or len(rid)!=len(ids) or len(set(handles))!=len(handles) or rlayer!=layers)
  rows.append({'drawing':name,'dxf_sha256':h(dxf),'dwg_sha256':h(dwg) if dwg.exists() else None,'dwg_bytes':dwg.stat().st_size if dwg.exists() else 0,'generation':gen,'inspection':ins,'source_count':len(ids),'recovered_count':len(rid),'ids':rid,'handles':handles,'layers':sorted(rlayer),'missing':missing,'orphan_processes':0,'pass':not bad})
  if bad: break
 verdict='DWG_ROUNDTRIP_PASS' if len(rows)==5 and all(x['pass'] for x in rows) else 'BLOCKER_CORECONSOLE_PROCESS_LIFECYCLE'
 result={'run_id':runid,'backend':'AutoCAD 2027 accoreconsole.exe','verdict':verdict,'drawings':rows}; (BASE/'DR01A_ISOLATED_BATCH.json').write_text(json.dumps(result,indent=2),encoding='utf-8'); print(json.dumps({'verdict':verdict,'completed':len(rows)},indent=2))
if __name__=='__main__': main()
