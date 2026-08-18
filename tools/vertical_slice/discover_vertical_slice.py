
from __future__ import annotations
import argparse, ast, hashlib, json, os, re, subprocess, sys
from pathlib import Path
from datetime import datetime, timezone

DOMAINS={
"wall":("wall","muro"),"door":("door","puerta"),"window":("window","ventana"),
"room":("room","space","habitacion"),"properties":("property","properties","inspector","bim_property"),
"relationships":("relationship","relation","propagation","constraint"),"history":("history","undo","redo","action"),
"persistence":("persist","serializ","save","load","project_io","repository"),
"workspace2":("workspace2","workspace_2","workspace","workbench"),"selection":("selection","select","hit_test")}

def digest(path):
 h=hashlib.sha256()
 with path.open("rb") as f:
  for chunk in iter(lambda:f.read(1024*1024),b""):h.update(chunk)
 return h.hexdigest()

def write(path,text):
 path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding="utf-8",newline="\n")

def symbols(root):
 rows=[]
 for path in sorted((root/"src").rglob("*.py")):
  try:tree=ast.parse(path.read_text(encoding="utf-8"))
  except Exception:continue
  rel=path.relative_to(root).as_posix();module=path.relative_to(root/"src").with_suffix("").as_posix().replace("/",".")
  imports=[]
  for node in ast.walk(tree):
   if isinstance(node,ast.Import):imports.extend(a.name for a in node.names)
   elif isinstance(node,ast.ImportFrom):imports.append(node.module or "")
  for node in tree.body:
   if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
    methods=[]
    if isinstance(node,ast.ClassDef):
     methods=[c.name for c in node.body if isinstance(c,(ast.FunctionDef,ast.AsyncFunctionDef))]
    rows.append({"path":rel,"module":module,"symbol":node.name,"kind":type(node).__name__,"methods":methods,"imports":sorted(set(imports)),"line":node.lineno})
 return rows

def classify(rows):
 out={k:[] for k in DOMAINS}
 for row in rows:
  hay=" ".join([row["path"],row["module"],row["symbol"]," ".join(row["methods"])," ".join(row["imports"])]).lower()
  for domain,terms in DOMAINS.items():
   if any(t in hay for t in terms):out[domain].append(row)
 return out

def tests(root):
 pattern=re.compile("|".join(re.escape(t) for ts in DOMAINS.values() for t in ts),re.I);rows=[]
 for path in sorted((root/"tests").rglob("test*.py")):
  try:text=path.read_text(encoding="utf-8")
  except Exception:continue
  hits=sorted(set(m.group(0).lower() for m in pattern.finditer(path.name+"\n"+text)))
  if hits:rows.append({"path":path.relative_to(root).as_posix(),"hits":hits})
 return rows

def run_tests(root,rows):
 selected=[r["path"] for r in rows[:80]]
 if not selected:return None
 env=os.environ.copy();env["PYTHONPATH"]=str(root/"src")+(os.pathsep+env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
 cmd=[sys.executable,"-m","pytest","-q",*selected]
 cp=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True,timeout=7200)
 return {"command":cmd,"selected_count":len(selected),"returncode":cp.returncode,"stdout":cp.stdout,"stderr":cp.stderr}

def main():
 ap=argparse.ArgumentParser();ap.add_argument("--root",default=".");ap.add_argument("--run-related-tests",action="store_true");ns=ap.parse_args()
 root=Path(ns.root).resolve()
 if not (root/"src").is_dir() or not (root/"tests").is_dir():print("ERROR: invalid AIAS root",file=sys.stderr);return 2
 out=root/"AIAS_L2_VERTICAL_SLICE_DISCOVERY_CURRENT";out.mkdir(parents=True,exist_ok=True)
 rows=symbols(root);groups=classify(rows);test_rows=tests(root);test_result=run_tests(root,test_rows) if ns.run_related_tests else None
 domains={}
 for name,items in groups.items():
  ranked=[]
  for row in items[:50]:
   score=(2 if row["kind"]=="ClassDef" else 0)+min(len(row["methods"]),5)
   key=(row["symbol"]+" "+row["path"]).lower()
   score+=sum(3 for t in DOMAINS[name] if t in key)
   ranked.append({**row,"score":score})
  ranked.sort(key=lambda r:(-r["score"],r["path"],r["line"]))
  domains[name]={"status":"DISCOVERED" if ranked else "MISSING","candidate_count":len(items),"recommended":ranked[:5]}
 missing=[k for k,v in domains.items() if v["status"]=="MISSING"]
 contract={"schema":"aias.l2.vertical-slice.discovery.v1","generated_at_utc":datetime.now(timezone.utc).isoformat(),"root":str(root),"symbol_count":len(rows),"related_test_count":len(test_rows),"domains":domains,"missing_domains":missing,"ready_for_implementation":not missing,"related_tests_returncode":None if test_result is None else test_result["returncode"]}
 gaps=[]
 for d in missing:gaps.append({"domain":d,"severity":"BLOCKER","action":"Provide authoritative adapter."})
 for d,v in domains.items():
  if len(v["recommended"])>1:gaps.append({"domain":d,"severity":"DECISION","candidates":[r["module"]+":"+r["symbol"] for r in v["recommended"]]})
 write(out/"SYMBOL_CATALOG.json",json.dumps(rows,ensure_ascii=False,indent=2)+"\n")
 write(out/"RELATED_TESTS.json",json.dumps({"tests":test_rows,"execution":test_result},ensure_ascii=False,indent=2)+"\n")
 write(out/"VERTICAL_SLICE_CONTRACT.json",json.dumps(contract,ensure_ascii=False,indent=2)+"\n")
 write(out/"INTEGRATION_GAPS.json",json.dumps(gaps,ensure_ascii=False,indent=2)+"\n")
 lines=["# AIAS L2 BIM Vertical Slice Discovery","",f"Generated: {contract['generated_at_utc']}","","## Summary",f"- Python symbols catalogued: **{len(rows)}**",f"- Related tests discovered: **{len(test_rows)}**",f"- Missing domains: **{len(missing)}**",f"- Ready for implementation: **{contract['ready_for_implementation']}**",f"- Related-test return code: **{contract['related_tests_returncode']}**","","## Domain status"]
 for d,v in domains.items():
  rec=v["recommended"][0] if v["recommended"] else None
  lines.append(f"- **{d}**: "+("MISSING" if rec is None else rec["module"]+":"+rec["symbol"]))
 write(out/"EXECUTIVE_REPORT.md","\n".join(lines)+"\n")
 write(out/"NEXT_IMPLEMENTATION_PLAN.md","# Next implementation plan\n\n1. Freeze one authoritative candidate per domain.\n2. Generate adapters.\n3. Implement the isolated vertical workflow.\n4. Add Undo/Redo and persistence round-trip tests.\n5. Connect Workspace 2.\n6. Run full regression and regenerate handoff.\n")
 checks=[]
 for p in sorted(out.iterdir()):
  if p.is_file() and p.name!="checksums.sha256":checks.append(f"{digest(p)} *{p.name}")
 write(out/"checksums.sha256","\n".join(checks)+"\n");print(out);return 0
if __name__=="__main__":raise SystemExit(main())
