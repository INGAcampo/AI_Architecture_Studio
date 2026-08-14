from __future__ import annotations
import hashlib, json

ORDER=["standards","analysis","reinforcement","cad","quantities","xlsx","reports","qa_qc","issuance_manifest"]
class RegenerationEngine:
    """Fingerprint-based, bounded downstream invalidation journal."""
    def fingerprint(self, value): return hashlib.sha256(json.dumps(value,sort_keys=True,default=str).encode()).hexdigest()
    def plan(self, before_graph, after_graph, prior_artifacts):
        before=self.fingerprint(before_graph.to_dict()); after=self.fingerprint(after_graph.to_dict())
        stale=[] if before==after else ORDER.copy()
        return {"graph_before":before,"graph_after":after,"changed":before!=after,"stale":stale,"order":stale,"prior_artifacts":prior_artifacts}
    def execute(self, plan, runners):
        journal=[]; artifacts={};
        if not plan["changed"]: return {"status":"NO_CHANGE","artifacts":artifacts,"journal":journal}
        try:
            for key in plan["order"]:
                value=runners[key](); digest=self.fingerprint(value); artifacts[key]={"sha256":digest,"value":value}; journal.append({"artifact":key,"status":"REGENERATED","sha256":digest})
        except Exception as exc:
            journal.append({"status":"ABORTED","reason":str(exc)}); return {"status":"ABORTED","artifacts":{},"journal":journal}
        return {"status":"PASS","artifacts":artifacts,"journal":journal}
