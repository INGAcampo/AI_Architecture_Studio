"""Dashboard snapshot and HTML release orchestration."""
from __future__ import annotations
import hashlib,json,zipfile
from pathlib import Path
from .collector import collect
from .renderer import render

class ProductivityDashboardOrchestrator:
 """Generate permanent machine-readable and visual productivity evidence."""
 def execute(self,root:Path,output:Path)->dict:
  """Collect repository evidence, render the panel and package a release."""
  output.mkdir(parents=True,exist_ok=True);data=collect(root);snapshot=output/"AIAS_PRODUCTIVITY_SNAPSHOT.json";panel=output/"AIAS_PRODUCTIVITY_DASHBOARD.html";snapshot.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");panel.write_text(render(data),encoding="utf-8");archive=output/"AIAS_PRODUCTIVITY_DASHBOARD_1.0.0.zip"
  with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as bundle:bundle.write(snapshot,snapshot.name);bundle.write(panel,panel.name)
  digest=hashlib.sha256(archive.read_bytes()).hexdigest();(output/f"{archive.name}.sha256").write_text(f"{digest}  {archive.name}\n",encoding="utf-8")
  return {"validated":True,"panel":str(panel),"snapshot":str(snapshot),"archive":str(archive),"sha256":digest,"components":data["capital"]["components"],"acceleration":data["acceleration"],"maturity":data["maturity"]}
