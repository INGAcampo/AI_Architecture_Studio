"""ATO analysis joining observations, governance and lifecycle evidence."""
from __future__ import annotations
import json
from pathlib import Path
from .governance import evaluate
from .materialization import earliest_action
from .scoring import score
from .sources import Observation,authoritative

class TechnologyObservatoryEngine:
    """Transform an authoritative observation into a governed opportunity."""
    def analyze(self,observation:Observation,foundation_dossier:Path,dimensions:dict)->dict:
        """Score an observation and connect admitted knowledge to a concrete AIAS consumer."""
        if not authoritative(observation):raise ValueError("unverifiable_source")
        dossier=json.loads(foundation_dossier.read_text(encoding="utf-8")); scored=score(evidence=observation.evidence_strength,**dimensions)
        governance=evaluate(True,True,True,True,"CONDITIONAL_REFERENCE_ONLY")
        opportunity_id=f"ATO-{observation.sha256[:12].upper()}"
        return {"opportunity_id":opportunity_id,"observation":observation.to_dict(),"score":scored,"governance":governance,"materialization":earliest_action(opportunity_id,governance["accepted"],scored["giant_step"]),"consumer_context":{"source_handover":dossier["handover_id"],"maturity_level":dossier["maturity"]["level"],"open_findings":len(dossier["findings"])}}
