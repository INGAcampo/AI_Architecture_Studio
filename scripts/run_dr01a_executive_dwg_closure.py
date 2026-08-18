"""Reproducible five-sheet native DWG certification for DR-01A."""
from __future__ import annotations
import hashlib, json, subprocess, time
from pathlib import Path
from aias_cad_professional.engine import CADDocument
from aias_dxf_writer import ValidDxfWriter

ROOT=Path(__file__).resolve().parents[1]
AUTO=Path(r"C:\Program Files\Autodesk\AutoCAD 2027\accoreconsole.exe")
BASE=ROOT/'engineering/aias/dependency_resolution/DR-01A_EXECUTIVE_DWG_CLOSURE'
MODEL=ROOT/'engineering/aias/professional_project_production/PRO-02_PROFESSIONAL_CAD_DRAWING_ENGINE/PILOT-BUILDING-001_CAD_V0.json'
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def cp(p): return str(Path(p).resolve()).replace('\\','/')
def invoke(drawing, script, tag, timeout=45):
 script_path=drawing.parent/(drawing.stem+'_'+tag+'.scr'); script_path.write_text(script,encoding='ascii'); started=time.time(); p=subprocess.Popen([str(AUTO),'/i',str(drawing),'/s',str(script_path)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 try: out,err=p.communicate(timeout=timeout); timed=False
 except subprocess.TimeoutExpired: p.kill(); out,err=p.communicate(); timed=True
 return {'pid':p.pid,'duration_seconds':round(time.time()-started,3),'timeout_seconds':timeout,'timed_out':timed,'exit_code':p.returncode,'stdout_tail':out[-1500:],'stderr_tail':err[-1500:]}
def inspect_script(log):
 return f'''(setq f (open "{cp(log)}" "w"))
(setq e (entnext))
(while e (setq d (entget e (list "AIAS")) x (cdr (assoc -3 d)) a (assoc "AIAS" x) i (if a (cdr (assoc 1000 (cdr a))) "")) (write-line (strcat "E|" i "|" (cdr (assoc 0 d)) "|" (if (assoc 8 d) (cdr (assoc 8 d)) "") "|" (cdr (assoc 5 d))) f) (setq e (entnext e)))
(close f)
(princ)
_.QUIT
'''
def main():
 if not AUTO.exists(): raise SystemExit('BLOCKED_BACKEND_UNAVAILABLE')
 doc=CADDocument(**json.loads(MODEL.read_text(encoding='utf-8'))); writer=ValidDxfWriter(); source_ids={e['id'] for e in doc.entities}; expected_layers={x['name'] for x in doc.layers}; out=BASE/'output'; source=out/'source'; native=out/'native'; source.mkdir(parents=True,exist_ok=True); native.mkdir(parents=True,exist_ok=True)
 rows=[]
 for sheet in doc.sheets:
  name=sheet['number']; dxf=source/(name+'.dxf'); mapping=writer.write(doc,dxf); dwg=native/(name+'.dwg')
  save= f'_.SAVEAS\n2018\n"{cp(dwg)}"\n_.QUIT\n'; save_result=invoke(dxf,save,'save')
  log=native/(name+'_inspect.txt'); log.unlink(missing_ok=True); reopen_result=invoke(dwg,inspect_script(log),'inspect') if dwg.exists() else {'exit_code':None,'timed_out':False}
  recovered=[]
  if log.exists():
   for line in log.read_text(encoding='utf-8',errors='replace').splitlines():
    parts=line.split('|');
    if len(parts)==5 and parts[0]=='E': recovered.append({'aias_id':parts[1],'type':parts[2],'layer':parts[3],'handle':parts[4]})
  ids=[x['aias_id'] for x in recovered if x['aias_id']]; handles=[x['handle'] for x in recovered if x['aias_id']]; recovered_layers={x['layer'] for x in recovered if x['aias_id']}
  missing=sorted(source_ids-set(ids)); unexpected=sorted(set(ids)-source_ids); duplicate_ids=sorted({x for x in ids if ids.count(x)>1}); duplicate_handles=sorted({x for x in handles if handles.count(x)>1})
  critical=bool(missing or unexpected or duplicate_ids or duplicate_handles or recovered_layers != expected_layers or save_result['exit_code']!=0 or reopen_result['exit_code']!=0 or save_result['timed_out'] or reopen_result['timed_out'])
  rows.append({'filename':dwg.name,'dwg_bytes':dwg.stat().st_size if dwg.exists() else 0,'dwg_sha256':digest(dwg) if dwg.exists() else None,'source_entity_count':len(source_ids),'reopened_entity_count':len(ids),'source_layers':sorted(expected_layers),'reopened_layers':sorted(recovered_layers),'aias_ids_source':sorted(source_ids),'aias_ids_recovered':sorted(ids),'handles':handles,'mapping':[{'aias_id':x['aias_id'],'handle':x['handle']} for x in recovered if x['aias_id']],'duplicate_ids':duplicate_ids,'missing_ids':missing,'unexpected_ids':unexpected,'critical_loss':critical,'degradations':['EXPECTED_MAPPING: blocks/dimensions are explicit TEXT/LINE equivalents; rectangles are polylines'],'save':save_result,'reopen':reopen_result,'source_dxf_sha256':digest(dxf),'dxf_mapping':mapping})
 verdict='DWG_ROUNDTRIP_PASS' if len(rows)==5 and all(not x['critical_loss'] and x['reopened_entity_count']==13 for x in rows) else 'BLOCKER_DWG_ROUNDTRIP_CERTIFICATION_FAILED'
 manifest={'backend':'AutoCAD 2027 accoreconsole.exe','version':'ACADVER 26.0','verdict':verdict,'drawings':rows}; BASE.mkdir(parents=True,exist_ok=True); (BASE/'DR01A_NATIVE_DWG_ROUNDTRIP.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8'); (BASE/'DR01A_DWG_MANIFEST.json').write_text(json.dumps({'verdict':verdict,'drawings':[{'filename':x['filename'],'sha256':x['dwg_sha256'],'bytes':x['dwg_bytes']} for x in rows]},indent=2),encoding='utf-8'); (BASE/'DR01A_NATIVE_DWG_ROUNDTRIP.md').write_text('# DR-01A Native DWG Roundtrip\n\nVerdict: `'+verdict+'`\n\nFive drawings were generated by AutoCAD Core Console from valid DXF and independently reopened with XData/APPID identity recovery.\n',encoding='utf-8'); print(json.dumps({'verdict':verdict,'drawings':len(rows)},indent=2))
if __name__=='__main__': main()
