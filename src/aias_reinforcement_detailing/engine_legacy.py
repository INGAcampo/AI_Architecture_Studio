from __future__ import annotations
from dataclasses import dataclass, asdict, field
import hashlib, json, math

@dataclass
class ReinforcementModel:
    project_id: str
    bar_sets: list[dict] = field(default_factory=list)
    schedules: list[dict] = field(default_factory=list)
    findings: list[dict] = field(default_factory=list)
    analysis_evidence_sha256: str = ""
    standards_evidence_sha256: str = ""
    design_evidence_sha256: str = ""
    schema: str = "aias.reinforcement_model.v1"

class ReinforcementEngine:
    """Evidence-bound reinforcement model; calculated As is never an executable detail by itself."""
    def build(self, structural_result, standards_evidence: dict, project_id="PILOT-BUILDING-001") -> ReinforcementModel:
        if not standards_evidence or not standards_evidence.get("pack"): raise ValueError("INSUFFICIENT_EVIDENCE: standards pack required")
        if structural_result is None or getattr(structural_result, "status", None) != "PASS":
            raise ValueError("INSUFFICIENT_EVIDENCE: passing structural analysis required")
        analysis_sha = getattr(structural_result, "evidence_sha256", "")
        if len(analysis_sha) != 64:
            raise ValueError("INSUFFICIENT_EVIDENCE: analysis SHA-256 required")
        standards_sha = sha(standards_evidence)
        result=ReinforcementModel(
            project_id,
            analysis_evidence_sha256=analysis_sha,
            standards_evidence_sha256=standards_sha,
        )
        # Sort by canonical element id so JSON round-trips cannot change design order.
        for eid, check in sorted(structural_result.design_checks.items()):
            kind=check["element_type"]
            if kind not in {"beam","column","slab","foundation"}:
                result.findings.append({"element_id":eid,"status":"BLOCKED","message":f"detail rule unavailable for {kind}"}); continue
            as_req=max(0.0, structural_result.reinforcement[eid]["ast_mm2"])
            diameter=16 if kind in {"beam","column","foundation"} else 10
            area=math.pi*diameter**2/4; qty=max(2,math.ceil(as_req/area)); length=4.0 if kind != "foundation" else 2.0
            status="PRELIMINARY" if standards_evidence.get("constructive_detailing") is not True else "DETAIL_READY"
            common={"element_id":eid,"element_type":kind,"status":status,"diameter_mm":diameter,"cover_mm":40,"development_length_mm":40*diameter,"lap_length_mm":50*diameter,"hook":"90deg","rule":standards_evidence["pack"],"calculated_as_mm2":as_req,"analysis_evidence_sha256":analysis_sha,"standards_evidence_sha256":standards_sha}
            result.bar_sets.append(self._bar_set(f"{eid}-LONG", "longitudinal", qty, length, 0, common))
            if kind in {"beam","column"}: result.bar_sets.append(self._bar_set(f"{eid}-TIES", "transverse", max(1,math.ceil(length/0.15)), 1.2, 150, common))
            if kind == "slab": result.bar_sets.append(self._bar_set(f"{eid}-TOP", "top", qty, length, 200, common))
        for bar in result.bar_sets:
            kg=bar["quantity"]*bar["length_m"]*(bar["diameter_mm"]**2/162); result.schedules.append({"bar_mark":bar["bar_mark"],"element_id":bar["element_id"],"diameter_mm":bar["diameter_mm"],"quantity":bar["quantity"],"length_m":bar["length_m"],"weight_kg":round(kg,3),"status":bar["status"],"bar_set_sha256":bar["sha256"],"analysis_evidence_sha256":analysis_sha,"standards_evidence_sha256":standards_sha})
        result.design_evidence_sha256 = sha({
            "project_id": result.project_id,
            "bar_sets": result.bar_sets,
            "schedules": result.schedules,
            "findings": result.findings,
            "analysis_evidence_sha256": analysis_sha,
            "standards_evidence_sha256": standards_sha,
        })
        return result

    def _bar_set(self, mark, role, quantity, length, spacing, common):
        bar={"bar_mark":mark,"role":role,"quantity":quantity,"length_m":length,"spacing_mm":spacing,"shape":"straight","position":role,**common}; bar["sha256"]=sha(bar); return bar

    def cad_details(self, model: ReinforcementModel) -> list[dict]:
        return [{"id":f"detail-{bar['bar_mark']}","kind":"reinforcement_annotation","bar_mark":bar["bar_mark"],"element_id":bar["element_id"],"status":bar["status"],"sha256":bar["sha256"]} for bar in model.bar_sets]

    def total_steel_kg(self, model): return round(sum(x["weight_kg"] for x in model.schedules),3)

def sha(value): return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),default=str).encode()).hexdigest()
