"""AST-based documentation coverage audit with hash-bound external references."""
from __future__ import annotations
import ast,hashlib,json
from pathlib import Path

def _public_symbols(tree: ast.Module):
 """Yield public top-level functions/classes and public methods with qualified names."""
 for node in tree.body:
  if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and not node.name.startswith("_"):
   yield node,node.name,"public_symbol"
   if isinstance(node,ast.ClassDef):
    for child in node.body:
     if isinstance(child,(ast.FunctionDef,ast.AsyncFunctionDef)) and not child.name.startswith("_"):
      yield child,f"{node.name}.{child.name}","public_method"

def _external(root:Path)->dict:
 path=root/"docs/reference/AIAS_PUBLIC_API_MANIFEST.json"
 if not path.is_file():return {}
 try:data=json.loads(path.read_text(encoding="utf-8"))
 except (OSError,json.JSONDecodeError):return {}
 rows={}
 for row in data.get("entries",[]):
  source=root/row.get("path","")
  if not source.is_file():continue
  digest=hashlib.sha256(source.read_bytes()).hexdigest()
  if digest==row.get("source_sha256"):rows[row["path"]]=row
 return rows

def audit(root:Path)->dict:
 """Measure inline or hash-bound external documentation coverage under ``root/src``."""
 modules=module_docs=symbols=symbol_docs=0;missing=[];external=_external(root)
 for path in sorted((root/"src").glob("aias_*/*.py")):
  try:tree=ast.parse(path.read_text(encoding="utf-8"))
  except (SyntaxError,UnicodeDecodeError):continue
  relative=path.relative_to(root).as_posix();record=external.get(relative,{})
  modules+=1
  if ast.get_docstring(tree) or record.get("module_documented"):module_docs+=1
  else:missing.append({"kind":"module","path":relative})
  documented=set(record.get("symbols",[]))
  for node,name,kind in _public_symbols(tree):
   symbols+=1
   if ast.get_docstring(node) or name in documented:symbol_docs+=1
   else:missing.append({"kind":kind,"path":relative,"symbol":name})
 return {"modules":modules,"documented_modules":module_docs,"module_coverage":module_docs/modules if modules else 1.0,"public_symbols":symbols,"documented_public_symbols":symbol_docs,"public_symbol_coverage":symbol_docs/symbols if symbols else 1.0,"complete":not missing,"missing":missing}

def audit_packages(root:Path,packages:tuple[str,...])->dict:
 """Measure documentation only for an explicit set of source packages."""
 overall=audit(root);rows=[]
 for package in packages:
  package_paths={p.relative_to(root).as_posix() for p in (root/"src"/package).glob("*.py")}
  missing=[m for m in overall["missing"] if m["path"] in package_paths]
  modules=len(package_paths);documented_modules=modules-sum(m["kind"]=="module" for m in missing)
  package_symbols=0;documented_symbols=0;external=_external(root)
  for path in sorted((root/"src"/package).glob("*.py")):
   tree=ast.parse(path.read_text(encoding="utf-8"));relative=path.relative_to(root).as_posix();record=external.get(relative,{})
   documented=set(record.get("symbols",[]))
   for node,name,_ in _public_symbols(tree):
    package_symbols+=1
    if ast.get_docstring(node) or name in documented:documented_symbols+=1
  rows.append({"package":package,"modules":modules,"documented_modules":documented_modules,"public_symbols":package_symbols,"documented_public_symbols":documented_symbols,"complete":not missing,"missing":missing})
 return {"packages":rows,"all_complete":all(row["complete"] for row in rows),"missing_count":sum(len(row["missing"]) for row in rows)}

def require_documented_packages(root:Path,packages:tuple[str,...])->None:
 """Raise a quality-gate error if a governed package has documentation debt."""
 result=audit_packages(root,packages)
 if not result["all_complete"]:raise ValueError(f"documentation_gate_failed:{result['missing_count']}")
