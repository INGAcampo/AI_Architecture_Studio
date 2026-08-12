"""Build auditable ATO portfolios, source ledgers, adapters and releases."""
from __future__ import annotations
import hashlib,json,zipfile
from pathlib import Path
from aias_foundation_handover.orchestrator import FoundationHandoverOrchestrator
from .catalog import initial_observations
from .engine import TechnologyObservatoryEngine

class TechnologyObservatoryOrchestrator:
    """Consume ECP-F evidence and emit the governed technology portfolio."""
    VERSION="1.0.0"
    def execute(self,workspace:Path,dossier:Path|None=None)->dict:
        """Evaluate observations and package reproducible observatory evidence."""
        workspace.mkdir(parents=True,exist_ok=True)
        if dossier is None:
            upstream=workspace/"source_ecp000001f";FoundationHandoverOrchestrator().execute(upstream);dossier=upstream/"lifecycle_dossier"/"FOUNDATION_HANDOVER_DOSSIER.json"
        dimensions={"relevance":.95,"impact":.9,"reuse":.9,"acceleration":.8,"risk":.2}
        opportunities=[TechnologyObservatoryEngine().analyze(item,dossier,dimensions) for item in initial_observations()]
        accepted=[item for item in opportunities if item["governance"]["accepted"]]
        output=workspace/"observatory";output.mkdir(exist_ok=True)
        portfolio={"observatory":"AIAS Technology Observatory","version":self.VERSION,"mission":"Explore world knowledge for giant, sustainable AIAS advances.","governing_article":"AEC-000049","opportunities":opportunities,"accepted_count":len(accepted),"immediate_actions":[item["materialization"] for item in accepted]}
        portfolio_path=output/"ATO_OPPORTUNITY_PORTFOLIO.json";portfolio_path.write_text(json.dumps(portfolio,indent=2)+"\n",encoding="utf-8")
        (output/"ATO_SOURCE_LEDGER.json").write_text(json.dumps([o.to_dict() for o in initial_observations()],indent=2)+"\n",encoding="utf-8")
        adapter={"adapter_id":"ATO-NIST-AIRMF-000001","status":"MATERIALIZED_REFERENCE_CAPABILITY","source":"https://airc.nist.gov/airmf-resources/airmf/5-sec-core/","crosswalk":{"GOVERN":["AEC-000002","AEC-000049"],"MAP":["ASDD","TRACEABILITY"],"MEASURE":["QUALITY_GATES","KPI_EVIDENCE"],"MANAGE":["ACE_NEXT_TASK","IMMEDIATE_ACTIONS"]},"legal_status":"VOLUNTARY_REFERENCE_FRAMEWORK"}
        (output/"ATO_NIST_AIRMF_ADAPTER.json").write_text(json.dumps(adapter,indent=2)+"\n",encoding="utf-8")
        release=workspace/"release";release.mkdir(exist_ok=True);archive=release/f"ECP-000001G_AIAS_TECHNOLOGY_OBSERVATORY_{self.VERSION}.zip"
        with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as bundle:
            for path in output.rglob("*"):
                if path.is_file():bundle.write(path,path.relative_to(output))
        digest=hashlib.sha256(archive.read_bytes()).hexdigest();(release/f"{archive.name}.sha256").write_text(f"{digest}  {archive.name}\n",encoding="utf-8")
        return {"validated":True,"observations":len(opportunities),"accepted":len(accepted),"giant_steps":sum(o["score"]["giant_step"] for o in accepted),"immediate_actions":len(portfolio["immediate_actions"]),"archive":str(archive),"sha256":digest}
