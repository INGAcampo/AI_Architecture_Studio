"""End-to-end reference orchestration and checksum-protected kernel release."""
from __future__ import annotations
from pathlib import Path
import json,zipfile,hashlib
from .reference_cases import build_reference_object, run_reference_cases
from .serialization import EngineeringObjectSerializer
from .traceability import TraceabilityEngine
from .state import StateMachine
from .adapters import ECFAdapter

class EngineeringObjectOrchestrator:
    """Execute the isolated-footing lifecycle and produce its technical evidence pack."""
    def execute_reference_flow(self, workspace: Path) -> dict:
        """Run the footing lifecycle and release its object, QA and trace evidence."""
        workspace.mkdir(parents=True,exist_ok=True)
        obj=build_reference_object()
        sm=StateMachine()
        sm.transition(obj.state,"VALIDATED")
        pressure=ECFAdapter().bearing_pressure(obj)
        obj.metadata["bearing_pressure_kpa"]=pressure
        sm.transition(obj.state,"CALCULATED")
        sm.transition(obj.state,"QA_PASSED")
        sm.transition(obj.state,"DOCUMENTED")

        object_path=EngineeringObjectSerializer().save(obj,workspace/"objects"/f"{obj.object_id}.json")
        trace_path=workspace/"traceability"/f"{obj.object_id}.json"
        trace_path.parent.mkdir(parents=True,exist_ok=True)
        trace_path.write_text(json.dumps(TraceabilityEngine().matrix(obj),indent=2),encoding="utf-8")

        cases=run_reference_cases()
        qa_path=workspace/"qa"/"reference_cases.json"
        qa_path.parent.mkdir(parents=True,exist_ok=True)
        qa_path.write_text(json.dumps({"passed":all(c["passed"] for c in cases),"cases":cases},indent=2),encoding="utf-8")
        if not all(c["passed"] for c in cases):
            raise RuntimeError("reference_cases_failed")

        technical=workspace/"technical_file"/"technical_file.json"
        technical.parent.mkdir(parents=True,exist_ok=True)
        technical.write_text(json.dumps({
            "program":"AMP-010C",
            "object_id":obj.object_id,
            "object_type":obj.object_type,
            "status":"READY_FOR_INTEGRATION",
            "bearing_pressure_kpa":pressure,
            "human_review_required":True
        },indent=2),encoding="utf-8")

        release=workspace/"release"
        release.mkdir(parents=True,exist_ok=True)
        archive=release/"AMP-010C_ENGINEERING_OBJECT_KERNEL_1.0.0.zip"
        with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
            for p in workspace.rglob("*"):
                if p.is_file() and release not in p.parents:
                    z.write(p,p.relative_to(workspace))
        return {
            "validated":True,
            "object_id":obj.object_id,
            "reference_cases":len(cases),
            "bearing_pressure_kpa":pressure,
            "archive":str(archive),
            "sha256":hashlib.sha256(archive.read_bytes()).hexdigest()
        }
