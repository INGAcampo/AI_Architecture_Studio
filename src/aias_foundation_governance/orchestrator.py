"""Validate and release the AIAS institutional foundations."""
from __future__ import annotations
import hashlib,json,zipfile
from pathlib import Path
from .validator import FoundationValidator
class FoundationGovernanceOrchestrator:
 """Load canonical foundation documents, validate them and create a release."""
 def execute(self,root:Path,output:Path)->dict:
  """Write validation evidence and a checksum-protected foundation archive."""
  charter_path=root/"engineering"/"aias"/"foundation"/"AIAS_CHARTER.json";handbook_path=root/"engineering"/"aias"/"foundation"/"AIAS_ARCHITECTURE_HANDBOOK.json";charter=json.loads(charter_path.read_text(encoding="utf-8"));handbook=json.loads(handbook_path.read_text(encoding="utf-8"));validator=FoundationValidator();errors=validator.validate_charter(charter)+validator.validate_handbook(handbook)
  output.mkdir(parents=True,exist_ok=True);evidence=output/"FOUNDATION_VALIDATION.json";evidence.write_text(json.dumps({"valid":not errors,"errors":errors,"charter":charter["id"],"handbook":handbook["id"]},indent=2)+"\n",encoding="utf-8")
  if errors:raise ValueError(errors)
  archive=output/"FOUNDATION_ALIGN_001_1.0.0.zip"
  with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as bundle:bundle.write(charter_path,charter_path.name);bundle.write(handbook_path,handbook_path.name);bundle.write(evidence,evidence.name)
  digest=hashlib.sha256(archive.read_bytes()).hexdigest();(output/f"{archive.name}.sha256").write_text(f"{digest}  {archive.name}\n",encoding="utf-8");return {"validated":True,"charter":charter["id"],"handbook":handbook["id"],"layers":len(handbook["layers"]),"rules":len(handbook["mandatory_rules"]),"archive":str(archive),"sha256":digest}
