"""Calculate an evidence-based package documentation priority plan."""
from __future__ import annotations
import ast,json
from pathlib import Path
CRITICAL={"aias_engineering_object":5,"aias_foundation_calcs":5,"aias_foundation_code_checks":5,"aias_foundation_objects":5,"aias_ecf":5,"aias_geometry_kernel":5,"aias_aeks":4,"aias_aeps_governance_sdd":5,"aias_foundation_delivery":5}
def build_plan(root:Path)->dict:
 """Inspect every AIAS package and rank missing documentation by risk and debt."""
 rows=[]
 for package in sorted((root/"src").glob("aias_*")):
  if not package.is_dir():continue
  modules=symbols=missing_modules=missing_symbols=0
  for path in package.glob("*.py"):
   try:tree=ast.parse(path.read_text(encoding="utf-8"))
   except (SyntaxError,UnicodeDecodeError):continue
   modules+=1;missing_modules+=not bool(ast.get_docstring(tree))
   for node in tree.body:
    if isinstance(node,(ast.ClassDef,ast.FunctionDef,ast.AsyncFunctionDef)) and not node.name.startswith("_"):
     symbols+=1;missing_symbols+=not bool(ast.get_docstring(node))
     if isinstance(node,ast.ClassDef):
      for method in node.body:
       if isinstance(method,(ast.FunctionDef,ast.AsyncFunctionDef)) and not method.name.startswith("_"):
        symbols+=1;missing_symbols+=not bool(ast.get_docstring(method))
  debt=missing_modules+missing_symbols
  if debt:rows.append({"package":package.name,"criticality":CRITICAL.get(package.name,2),"modules":modules,"symbols":symbols,"missing_modules":missing_modules,"missing_symbols":missing_symbols,"debt":debt,"risk_score":CRITICAL.get(package.name,2)*100+debt})
 rows.sort(key=lambda x:(-x["risk_score"],x["package"]))
 return {"program":"DOC-ALIGN-002","policy":"criticality_then_debt","package_count":len(rows),"total_debt":sum(x["debt"] for x in rows),"priority_queue":rows}
def write_plan(root:Path,output:Path)->dict:
 """Write the deterministic plan as machine-readable evidence."""
 plan=build_plan(root);output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(plan,indent=2)+"\n",encoding="utf-8");return plan
