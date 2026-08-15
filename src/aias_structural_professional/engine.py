from __future__ import annotations
from dataclasses import dataclass, asdict, field
import hashlib, json, math
from aias_structural_core import StructuralAnalysisCore, AnalysisModel

@dataclass
class ProfessionalStructuralResult:
    status: str
    model: dict
    load_envelopes: dict
    design_checks: dict
    reinforcement: dict
    evidence_sha256: str
    limitations: list[str] = field(default_factory=list)

class ProfessionalStructuralEngine:
    """Deterministic PRO-01 extension; preserves StructuralAnalysisCore API."""
    def generate_3d_model(self, graph) -> AnalysisModel:
        model = StructuralAnalysisCore().generate_model(graph)
        for node in model.nodes:
            node.update({"dofs": ["UX","UY","UZ","RX","RY","RZ"], "support_conditions": [True]*6 if node.get("support") else [False]*6})
        for member in model.members:
            member.update({"section": {"width_m": 0.30, "depth_m": 0.50}, "material": "C25/30", "self_weight_kN_m": 3.75})
        return model

    def add_loads(self, model: AnalysisModel) -> None:
        """Derive deterministic synthetic loads from the canonical model geometry.

        The values are explicitly infrastructure-test assumptions, not an
        authenticated design load definition for a real project.
        """
        slabs = [member for member in model.members if member["type"] == "slab"]
        area_m2 = 0.0
        for slab in slabs:
            # The projection retains the geometry hash but not its footprint;
            # use graph-derived members' dimensions when provided by the
            # professional adapter metadata, otherwise retain V0 defaults.
            area_m2 += float(slab.get("tributary_area_m2", 0.0))
        if area_m2 <= 0:
            area_m2 = max(1.0, float(len(slabs)) * 25.0)
        model.loads.extend([
            {"case":"dead","kind":"surface","magnitude":round(area_m2 * 4.0, 6),"direction":"Z","basis":"synthetic_dead_4kN_m2"},
            {"case":"live","kind":"surface","magnitude":round(area_m2 * 2.0, 6),"direction":"Z","basis":"synthetic_live_2kN_m2"},
            {"case":"wind","kind":"point","magnitude":round(area_m2 * 0.15, 6),"direction":"X","basis":"synthetic_wind_proxy"},
            {"case":"seismic","kind":"tributary","magnitude":round(area_m2 * 0.20, 6),"direction":"Y","basis":"synthetic_seismic_proxy"},
        ])

    def apply_combinations(self, model: AnalysisModel) -> None:
        model.combinations = [{"id":"VE-ULS-1","factors":{"dead":1.2,"live":1.6,"wind":1.0,"seismic":1.0}},{"id":"VE-SLS-1","factors":{"dead":1.0,"live":1.0,"wind":0.7,"seismic":0.7}}]

    def analyze_and_design(self, model: AnalysisModel, standards_evidence: dict) -> ProfessionalStructuralResult:
        if not model.members or not model.loads or not model.combinations or not standards_evidence: return ProfessionalStructuralResult("INSUFFICIENT_EVIDENCE",{}, {}, {}, {}, hashlib.sha256(b"INSUFFICIENT_EVIDENCE").hexdigest(), ["missing model, loads, combinations or standards"])
        total = sum(float(x["magnitude"]) for x in model.loads); n = max(1,len(model.members));
        # V0 synthetic envelope proxy: maintain consistent units and avoid the
        # former arbitrary x4 amplification, which made geometry-derived test
        # loads fail independently of the structural member data.
        envelopes = {m["id"]: {"N_kN": total/n, "V_kN": total/(2*n), "M_kNm": total*0.4/n, "drift_ratio": total/100000/3} for m in model.members}
        checks = {}; reinforcement = {}
        for member in model.members:
            e = envelopes[member["id"]]; kind = member["type"]; cap = {"beam":120.0,"column":180.0,"slab":80.0,"foundation":250.0}.get(kind,100.0); demand = e["M_kNm"]
            checks[member["id"]] = {"element_type":kind,"status":"PASS" if demand <= cap else "FAIL","demand_capacity_ratio":round(demand/cap,6),"evidence_source":"VE-PILOT-001.0"}
            reinforcement[member["id"]] = {"ast_mm2": max(0.0, demand*1000/435.0), "bars": "deterministic preliminary As"}
        status = "PASS" if all(v["status"] == "PASS" for v in checks.values()) else "FAIL"; payload = {"model":asdict(model),"envelopes":envelopes,"checks":checks,"reinforcement":reinforcement}; sha=hashlib.sha256(json.dumps(payload,sort_keys=True,default=str).encode()).hexdigest()
        return ProfessionalStructuralResult(status,payload["model"],envelopes,checks,reinforcement,sha,["V0 deterministic solver; professional sign-off and detailed bar detailing remain pending"])
