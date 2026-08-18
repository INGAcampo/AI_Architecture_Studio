"""Generate the complete canonical inventory and ordered materialization roadmap."""
from __future__ import annotations
import hashlib,json,zipfile
from pathlib import Path
from .catalog import concepts
from .evidence import reconcile
from .lighthouse import contract
from .roadmap import dependency_cycles,waves
from .validator import validate
class MasterInventoryOrchestrator:
 """Reconcile concepts with repository evidence and package the master plan."""
 def execute(self,root:Path,output:Path)->dict:
  """Write JSON/Markdown inventory, dependency roadmap and lighthouse contract."""
  output.mkdir(parents=True,exist_ok=True);rows=concepts();errors=validate(rows);cycles=dependency_cycles(rows)
  if errors or cycles:raise ValueError({"errors":errors,"cycles":cycles})
  reconciled=reconcile(root,rows);unsupported=[r["id"] for r in reconciled if not r["supported"]];roadmap=waves(reconciled);light=contract()
  data={"inventory_id":"AMIR-000001","version":"1.0.0","concept_count":len(rows),"state_counts":{s:sum(r["declared_state"]==s for r in rows) for s in sorted({r["declared_state"] for r in rows})},"unsupported_declarations":unsupported,"concepts":reconciled}
  files={"AIAS_MASTER_CONCEPT_INVENTORY.json":data,"AIAS_MATERIALIZATION_ROADMAP.json":{"waves":roadmap},"PROJECT_LIGHTHOUSE_001_CONTRACT.json":light}
  for name,value in files.items():(output/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
  lines=["# AIAS Master Concept Inventory","",f"Concepts: {len(rows)}","", "| ID | Kind | State | Wave | Evidence | Name |","|---|---|---|---:|---:|---|"]+[f"| {r['id']} | {r['kind']} | {r['declared_state']} | {r['wave']} | {'YES' if r['evidence_exists'] else 'NO'} | {r['name']} |" for r in reconciled]
  (output/"AIAS_MASTER_CONCEPT_INVENTORY.md").write_text("\n".join(lines)+"\n",encoding="utf-8");archive=output/"AMIR-000001_MASTER_INVENTORY_1.0.0.zip"
  with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as bundle:
   for path in output.glob("AIAS_*.*"):bundle.write(path,path.name)
   bundle.write(output/"PROJECT_LIGHTHOUSE_001_CONTRACT.json","PROJECT_LIGHTHOUSE_001_CONTRACT.json")
  digest=hashlib.sha256(archive.read_bytes()).hexdigest();(output/f"{archive.name}.sha256").write_text(f"{digest}  {archive.name}\n",encoding="utf-8")
  return {"validated":not unsupported,"concepts":len(rows),"unsupported":unsupported,"waves":len(roadmap),"lighthouse_deliverables":len(light["deliverables"]),"archive":str(archive),"sha256":digest}
