"""End-to-end technical-file generation, completeness and integrity packaging."""
from __future__ import annotations
import hashlib,json,zipfile
from pathlib import Path
from aias_drawing_framework import DrawingExporter
from aias_drawing_framework.reference import foundation_sheet
from aias_engineering_wave12 import FoundationProfessionalWorkflow
from aias_foundation_documentation.orchestrator import FoundationDocumentationOrchestrator
from aias_foundation_delivery.orchestrator import FoundationDeliveryOrchestrator
from aias_foundation_handover.orchestrator import FoundationHandoverOrchestrator
from .memory import build_memory,write_memory
from .models import ProjectBrief

class TechnicalFileGenerator:
    """Assemble calculations, checks, drawings, narrative, delivery and custody evidence."""
    REQUIRED=("descriptive_memory","engineering","drawings","documentation","coordination","handover","integrity_manifest")
    def generate(self,brief:ProjectBrief,workspace:Path)->dict:
        """Generate a complete FOR_REVIEW dossier and checksum-protected release."""
        brief.validate();workspace.mkdir(parents=True,exist_ok=True);content=workspace/"technical_file";content.mkdir(exist_ok=True)
        engineering=FoundationProfessionalWorkflow().execute(content/"engineering");drawings=DrawingExporter().export(foundation_sheet(),content/"drawings");documentation=FoundationDocumentationOrchestrator().execute(content/"documentation");coordination=FoundationDeliveryOrchestrator().execute(content/"coordination",content/"documentation",brief.revision);handover=FoundationHandoverOrchestrator().execute(content/"handover",content/"coordination/transmittal");memory=write_memory(build_memory(brief,engineering,drawings),content/"descriptive_memory")
        components={"descriptive_memory":memory,"engineering":engineering,"drawings":drawings,"documentation":documentation,"coordination":coordination,"handover":handover};manifest=self._manifest(content);manifest_path=content/"INTEGRITY_MANIFEST.json";manifest_path.write_text(json.dumps(manifest,indent=2)+"\n",encoding="utf-8");components["integrity_manifest"]={"path":str(manifest_path),"files":len(manifest["files"]),"root_sha256":manifest["root_sha256"]}
        completeness={key:key in components for key in self.REQUIRED};release=workspace/"release";release.mkdir(exist_ok=True);archive=release/f"{brief.project_id}_TECHNICAL_FILE_{brief.revision}.zip"
        with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as bundle:
            for path in sorted(content.rglob("*")):
                if path.is_file():bundle.write(path,path.relative_to(content))
        digest=hashlib.sha256(archive.read_bytes()).hexdigest();summary={"technical_file_id":f"TF-{brief.project_id}-{brief.revision}","project_id":brief.project_id,"revision":brief.revision,"status":"FOR_REVIEW","complete":all(completeness.values()),"completeness":completeness,"professional_review_required":True,"verified_official_jurisdiction_pack_required":True,"archive":str(archive),"sha256":digest,"components":components};(release/"TECHNICAL_FILE_SUMMARY.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2,default=str)+"\n",encoding="utf-8");return summary
    def _manifest(self,root:Path)->dict:
        files=[]
        for path in sorted(root.rglob("*")):
            if path.is_file() and path.name!="INTEGRITY_MANIFEST.json":files.append({"path":path.relative_to(root).as_posix(),"bytes":path.stat().st_size,"sha256":hashlib.sha256(path.read_bytes()).hexdigest()})
        canonical=json.dumps(files,sort_keys=True,separators=(",",":")).encode();return {"algorithm":"SHA-256","files":files,"root_sha256":hashlib.sha256(canonical).hexdigest()}
