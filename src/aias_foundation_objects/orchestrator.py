"""Reference-object generation, QA evidence and checksum release orchestration."""
from pathlib import Path
import json,zipfile,hashlib
from .reference_cases import reference_objects,run_reference_cases
from .serialization import FoundationSerializer
from .metrics import FoundationMetrics

class FoundationObjectOrchestrator:
    """Serialize all foundation families and package their technical summary."""
    def execute(self, workspace: Path) -> dict:
        """Generate all reference families and package QA, metrics and release evidence."""
        workspace.mkdir(parents=True,exist_ok=True)
        objs=reference_objects()
        serializer=FoundationSerializer()
        for name,obj in objs.items():
            serializer.save(obj,workspace/"objects"/f"{name}.json")
        cases=run_reference_cases()
        qa=workspace/"qa"/"reference_cases.json"; qa.parent.mkdir(parents=True,exist_ok=True)
        qa.write_text(json.dumps({"passed":all(c["passed"] for c in cases),"cases":cases},indent=2),encoding="utf-8")
        if not all(c["passed"] for c in cases):
            raise RuntimeError("reference_cases_failed")
        metrics=FoundationMetrics()
        summary={name:{
            "area_m2":obj.geometry.area_m2,
            "volume_m3":metrics.concrete_volume_m3(obj),
            "service_load_kn":metrics.total_service_load_kn(obj),
        } for name,obj in objs.items()}
        (workspace/"technical_file").mkdir(exist_ok=True)
        (workspace/"technical_file"/"summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
        rel=workspace/"release"; rel.mkdir(exist_ok=True)
        archive=rel/"ECP-000001A_FOUNDATION_OBJECT_LIBRARY_1.0.0.zip"
        with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as z:
            for p in workspace.rglob("*"):
                if p.is_file() and rel not in p.parents:
                    z.write(p,p.relative_to(workspace))
        return {"validated":True,"reference_cases":len(cases),"objects":len(objs),
                "archive":str(archive),"sha256":hashlib.sha256(archive.read_bytes()).hexdigest()}
