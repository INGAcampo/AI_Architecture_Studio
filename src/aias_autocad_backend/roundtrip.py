from pathlib import Path
import hashlib,json,subprocess

AUTOCAD=Path(r"C:\Program Files\Autodesk\AutoCAD 2027\accoreconsole.exe")
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run_roundtrip(source_dir, output_dir):
 source_dir,output_dir=Path(source_dir),Path(output_dir); output_dir.mkdir(parents=True,exist_ok=True)
 if not AUTOCAD.exists(): return {"verdict":"BLOCKED_BACKEND_UNAVAILABLE"}
 lisp=output_dir/'inspect.lsp'; lisp.write_text('(defun aias-log () (setq f (open "__LOG__" "w")) (setq e (entnext) n 0) (while e (setq d (entget e)) (write-line (strcat (cdr (assoc 0 d)) "|" (cdr (assoc 8 d)) "|" (cdr (assoc 5 d))) f) (setq n (+ n 1)) (setq e (entnext e))) (close f) (princ))',encoding='ascii')
 rows=[]
 for src in sorted(source_dir.glob('*.dxf')):
  dwg=output_dir/(src.stem+'.dwg'); save=output_dir/(src.stem+'_save.scr'); save.write_text(f'_.SAVEAS\n2018\n"{str(dwg).replace(chr(92),"/")}"\n_.QUIT\n',encoding='ascii')
  first=subprocess.run([str(AUTOCAD),'/i',str(src),'/s',str(save)],capture_output=True,text=True,timeout=90)
  log=output_dir/(src.stem+'_reopen.log'); lisp_text=lisp.read_text(encoding='ascii').replace('__LOG__',str(log).replace('\\','/')); inspect=output_dir/(src.stem+'_inspect.scr'); inspect.write_text(f'{lisp_text}\n(aias-log)\n_.QUIT\n',encoding='ascii')
  second=subprocess.run([str(AUTOCAD),'/i',str(dwg),'/s',str(inspect)],capture_output=True,text=True,timeout=90) if dwg.exists() else None
  recovered=log.read_text(encoding='utf-8',errors='replace').splitlines() if log.exists() else []
  rows.append({"source":src.name,"dwg":dwg.name,"source_sha256":sha(src),"dwg_sha256":sha(dwg) if dwg.exists() else None,"source_entities":src.read_text(encoding='ascii',errors='ignore').count('\n0\n'),"reopened_entities":len(recovered),"types":sorted({x.split('|')[0] for x in recovered}),"layers":sorted({x.split('|')[1] for x in recovered if '|' in x}),"handles":{x.split('|')[2]:x.split('|')[0] for x in recovered if x.count('|')>=2},"first_exit":first.returncode,"second_exit":None if second is None else second.returncode,"first_log":first.stdout[-1000:],"second_log":"" if second is None else second.stdout[-1000:]})
 verdict='DWG_ROUNDTRIP_PASS' if rows and all(r['dwg_sha256'] and r['second_exit']==0 and r['reopened_entities']>0 for r in rows) else 'BLOCKER_REOPEN_OR_SAVE_DWG'
 return {"backend":"AutoCAD 2027 accoreconsole.exe","verdict":verdict,"drawings":rows}
