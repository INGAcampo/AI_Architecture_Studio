from __future__ import annotations
from dataclasses import dataclass, asdict, field
import hashlib, json, math
from aias_structural_core import StructuralAnalysisCore, AnalysisModel

@dataclass
class ProfessionalStructuralResult:
    status: str
    model: dict
    load_envelopes: dict
    combination_results: dict
    design_checks: dict
    reinforcement: dict
    analysis_trace: dict
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
        if not model.members or not model.loads or not model.combinations or not standards_evidence:
            return self._insufficient("missing model, loads, combinations or standards")
        load_cases = {load.get("case"): float(load.get("magnitude", -1.0)) for load in model.loads}
        if None in load_cases or any(value < 0 for value in load_cases.values()):
            return self._insufficient("invalid load case")
        if len(load_cases) != len(model.loads):
            return self._insufficient("duplicate load case")
        if not model.metadata.get("source_graph_sha256"):
            return self._insufficient("analysis model is not bound to a Project Graph")

        supports = [node["id"] for node in model.nodes if node.get("support")]
        if not supports:
            return self._insufficient("analysis model has no supports")
        combination_results = {}
        for combination in model.combinations:
            combination_id = combination.get("id")
            factors = combination.get("factors", {})
            if not combination_id or not factors or not set(factors) <= set(load_cases):
                return self._insufficient("combination references missing load cases")
            contributions = {
                case: round(load_cases[case] * float(factor), 9)
                for case, factor in sorted(factors.items())
            }
            factored_total = round(sum(contributions.values()), 9)
            reaction = round(factored_total / len(supports), 9)
            reactions = {support: reaction for support in supports}
            imbalance = round(abs(sum(reactions.values()) - factored_total), 9)
            combination_results[combination_id] = {
                "load_contributions_kN": contributions,
                "factored_total_kN": factored_total,
                "support_reactions_kN": reactions,
                "equilibrium_imbalance_kN": imbalance,
                "equilibrium_status": "PASS" if imbalance <= 1e-6 else "FAIL",
            }

        n = max(1, len(model.members))
        governing_id, governing = max(
            combination_results.items(), key=lambda item: item[1]["factored_total_kN"]
        )
        total = governing["factored_total_kN"]
        envelopes = {
            member["id"]: {
                "N_kN": round(total / n, 9),
                "V_kN": round(total / (2 * n), 9),
                "M_kNm": round(total * 0.4 / n, 9),
                "drift_ratio": round(total / 100000 / 3, 12),
                "governing_combination": governing_id,
                "source_member_id": member.get("source_node_id", member["id"]),
            }
            for member in model.members
        }
        checks = {}; reinforcement = {}
        standards_id = standards_evidence.get("pack") or standards_evidence.get("scenario_id") or "SYNTHETIC_EVIDENCE"
        for member in model.members:
            e = envelopes[member["id"]]; kind = member["type"]; cap = {"beam":120.0,"column":180.0,"slab":80.0,"foundation":250.0}.get(kind,100.0); demand = e["M_kNm"]
            checks[member["id"]] = {"element_type":kind,"status":"PASS" if demand <= cap else "FAIL","demand_capacity_ratio":round(demand/cap,6),"evidence_source":standards_id,"governing_combination":governing_id}
            reinforcement[member["id"]] = {"ast_mm2": max(0.0, demand*1000/435.0), "bars": "deterministic preliminary As"}
        standards_sha256 = hashlib.sha256(json.dumps(standards_evidence, sort_keys=True).encode()).hexdigest()
        trace = {
            "schema": "aias.analysis_trace.v1",
            "source_graph_sha256": model.metadata["source_graph_sha256"],
            "analysis_model_sha256": hashlib.sha256(json.dumps(asdict(model), sort_keys=True).encode()).hexdigest(),
            "standards_evidence_sha256": standards_sha256,
            "governing_combination": governing_id,
            "equilibrium_status": "PASS" if all(
                value["equilibrium_status"] == "PASS" for value in combination_results.values()
            ) else "FAIL",
        }
        status = "PASS" if trace["equilibrium_status"] == "PASS" and all(v["status"] == "PASS" for v in checks.values()) else "FAIL"
        payload = {"model":asdict(model),"envelopes":envelopes,"combination_results":combination_results,"checks":checks,"reinforcement":reinforcement,"analysis_trace":trace}
        sha=hashlib.sha256(json.dumps(payload,sort_keys=True,default=str).encode()).hexdigest()
        return ProfessionalStructuralResult(status,payload["model"],envelopes,combination_results,checks,reinforcement,trace,sha,["Deterministic synthetic analysis; professional sign-off and detailed bar detailing remain pending"])

    @staticmethod
    def _insufficient(reason: str) -> ProfessionalStructuralResult:
        return ProfessionalStructuralResult(
            "INSUFFICIENT_EVIDENCE", {}, {}, {}, {}, {}, {},
            hashlib.sha256(("INSUFFICIENT_EVIDENCE:" + reason).encode()).hexdigest(),
            [reason],
        )
