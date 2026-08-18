"""Reference code-check execution, QA evidence and checksum release packaging."""
from pathlib import Path
import json,zipfile,hashlib
from .reference_pack import generic_reference_pack,reference_input
from .engine import FoundationCodeCheckEngine
from .reference_cases import run_reference_cases
from .reporting import CodeCheckReportWriter

class FoundationCodeCheckOrchestrator:
    """Produce a reproducible reference-only foundation verification technical file."""
    def execute(self,workspace:Path)->dict:
        """Execute reference checks and package technical, QA and release evidence."""
        workspace.mkdir(parents=True,exist_ok=True)
        pack=generic_reference_pack(); data=reference_input()
        result=FoundationCodeCheckEngine().check(data,pack)
        CodeCheckReportWriter().write(data,result,workspace/"technical_file"/"foundation_code_check.json")
        cases=run_reference_cases()
        qa=workspace/"qa"/"reference_cases.json"; qa.parent.mkdir(parents=True,exist_ok=True)
        qa.write_text(json.dumps({"passed":all(c["passed"] for c in cases),"cases":cases},indent=2),encoding="utf-8")
        if not all(c["passed"] for c in cases): raise RuntimeError("reference_cases_failed")
        rel=workspace/"release"; rel.mkdir(exist_ok=True)
        archive=rel/"ECP-000001C_FOUNDATION_CODE_CHECK_FRAMEWORK_1.0.0.zip"
        with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
            for p in workspace.rglob("*"):
                if p.is_file() and rel not in p.parents:
                    z.write(p,p.relative_to(workspace))
        return {
            "validated":True,"reference_cases":len(cases),"checks":len(result.checks),
            "code_pack":pack.code_id,"legal_status":pack.legal_status,
            "archive":str(archive),"sha256":hashlib.sha256(archive.read_bytes()).hexdigest()
        }
