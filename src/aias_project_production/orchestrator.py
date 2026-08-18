from pathlib import Path
import json
from dataclasses import asdict
import hashlib

from aias_building_design_core import ArchitecturalProductionCore
from aias_building_design_core.core import BuildingDesignCore
from aias_building_design_core.native_bim import NativeBimProjection
from aias_structural_professional.engine import ProfessionalStructuralEngine
from aias_standards_core import ApplicabilityEngine, StandardsPack
from aias_reinforcement_detailing import ReinforcementEngine

from .adapters import (
    DrawingProductionAdapter,
    ExecutiveIssuanceAdapter,
    ProfessionalQAAdapter,
    QuantityWorkbookAdapter,
    ReportProductionAdapter,
)


class AIASProjectProductionOrchestrator:
    """Synthetic-only composition root for the canonical PP production contracts."""

    def __init__(self, output_root: str | Path):
        self.output_root = Path(output_root)
        self.drawing = DrawingProductionAdapter()
        self.quantities = QuantityWorkbookAdapter()
        self.reports = ReportProductionAdapter()
        self.qa = ProfessionalQAAdapter()
        self.issuance = ExecutiveIssuanceAdapter()

    def run(self, scenario_id: str, project_id: str = "PILOT-BUILDING-001", mode: str = "PILOT_SYNTHETIC", project_name: str | None = None, manifest: dict | None = None) -> dict:
        if scenario_id not in {"BEST_CASE_001", "NOMINAL_CASE_001", "STRESS_CASE_001"}:
            raise ValueError("unknown synthetic scenario")
        core = BuildingDesignCore()
        if mode not in {"PILOT_SYNTHETIC", "REAL_PROJECT"}: raise ValueError("invalid project mode")
        if mode == "REAL_PROJECT" and not (manifest and manifest.get("authenticated_provenance_sha256")):
            raise ValueError("AUTHENTICATED_EXTERNAL_INPUT_REQUIRED: REAL_PROJECT baseline is not authenticated")
        if manifest:
            from aias_project_intake.builders import ParametricProjectGraphBuilder
            graph = ParametricProjectGraphBuilder().build(manifest)
        else:
            graph = core.seed_pilot(core.create_project(project_name or f"{mode} {scenario_id}", project_id=project_id))
        errors = core.validate(graph)
        if errors:
            return {"verdict": "BLOCKED_SOFTWARE", "errors": errors}
        scenario_dir = self.output_root / scenario_id
        scenario_dir.mkdir(parents=True, exist_ok=True)
        graph_path = scenario_dir / "project_graph.json"
        graph.save(graph_path)
        architecture = None
        architecture_path = None
        architectural_core = ArchitecturalProductionCore()
        if manifest:
            architecture = architectural_core.materialize(graph)
            architecture_path = scenario_dir / "architectural_model.json"
            architecture_path.write_text(json.dumps(architecture, indent=2, sort_keys=True), encoding="utf-8")
        native_bim = NativeBimProjection().materialize(graph)
        native_bim_path = scenario_dir / 'native_bim_projection.json'
        native_bim_path.write_text(json.dumps(native_bim, indent=2, sort_keys=True), encoding='utf-8')
        standards = ApplicabilityEngine(StandardsPack())
        standards_context = {"project": graph.project_id, "jurisdiction": "VE", "SYNTHETIC_TEST_DATA": True, "NOT_FOR_CONSTRUCTION": True}
        standards_verdicts = {rule: standards.evaluate(rule, standards_context, {"source": "AIAS_SYNTHETIC", "value": scenario_id, "pass": True}).to_dict() for rule in StandardsPack().rules}
        structural = ProfessionalStructuralEngine()
        model = structural.generate_3d_model(graph)
        structural.add_loads(model)
        if scenario_id == "STRESS_CASE_001":
            for load in model.loads:
                load["magnitude"] *= 30.0
        structural.apply_combinations(model)
        synthetic_standards_evidence = {
            "pack": "AIAS-SYNTHETIC-ANALYSIS-001",
            "scenario_id": scenario_id,
            "SYNTHETIC_TEST_DATA": True,
            "NOT_FOR_CONSTRUCTION": True,
        }
        synthetic_standards_evidence["pack_sha256"] = hashlib.sha256(
            json.dumps(synthetic_standards_evidence, sort_keys=True).encode()
        ).hexdigest()
        synthetic_standards_evidence["rule_verdicts"] = standards_verdicts
        standards_path = scenario_dir / "standards_evidence.json"
        standards_path.write_text(json.dumps(synthetic_standards_evidence, indent=2, sort_keys=True), encoding="utf-8")
        result = structural.analyze_and_design(model, synthetic_standards_evidence)
        reinforcement = ReinforcementEngine().build(result, synthetic_standards_evidence, project_id=graph.project_id)
        reinforcement_path = scenario_dir / "reinforcement_model.json"
        reinforcement_path.write_text(json.dumps(asdict(reinforcement), indent=2, sort_keys=True), encoding="utf-8")
        structural_evidence = {
            "schema": "aias.structural_production_evidence.v1",
            "project_id": graph.project_id,
            "SYNTHETIC_TEST_DATA": True,
            "NOT_FOR_CONSTRUCTION": True,
            "analysis_model": asdict(model),
            "result": asdict(result),
            "source_graph_sha256": model.metadata["source_graph_sha256"],
            "projection": model.metadata.get("projection"),
        }
        structural_path = scenario_dir / "structural_production_evidence.json"
        structural_path.write_text(json.dumps(structural_evidence, indent=2, sort_keys=True), encoding="utf-8")
        structural_sha256 = hashlib.sha256(structural_path.read_bytes()).hexdigest()
        drawing = self.drawing.produce(
            graph, result, scenario_dir / "drawings", reinforcement_model=reinforcement
        )
        quantities = self.quantities.produce(graph, scenario_dir / "quantities")
        quantities["reinforcement"] = {
            "bar_set_count": len(reinforcement.bar_sets),
            "steel_kg": ReinforcementEngine().total_steel_kg(reinforcement),
            "schedule_sha256": hashlib.sha256(json.dumps(reinforcement.schedules, sort_keys=True).encode()).hexdigest(),
            "design_evidence_sha256": reinforcement.design_evidence_sha256,
            "status": "PRELIMINARY",
        }
        (scenario_dir / "quantities" / "reinforcement_schedule.json").write_text(
            json.dumps(quantities["reinforcement"], indent=2, sort_keys=True), encoding="utf-8"
        )
        coherence = None
        coherence_path = None
        if architecture is not None:
            coherence = architectural_core.verify_coherence(
                graph, architecture, model, drawing["model"], quantities["package"],
                native_bim=native_bim,
            )
            if coherence["verdict"] != "ARCHITECTURAL_PIPELINE_COHERENT":
                raise RuntimeError("BLOCKED_SOFTWARE: BIM/Analysis/Drawings/Quantities coherence failed")
            coherence_path = scenario_dir / "pipeline_coherence.json"
            coherence_path.write_text(json.dumps(coherence, indent=2, sort_keys=True), encoding="utf-8")
        reports = self.reports.produce(graph, result, drawing["model"], quantities["package"], scenario_dir / "reports")
        qa = self.qa.evaluate(result, drawing, quantities, reports, scenario_id)
        qa["reinforcement"] = quantities["reinforcement"]
        qa["drawing_trace"] = drawing["design_trace"]
        issuance = self.issuance.issue(scenario_id, scenario_dir, drawing, quantities, reports, qa)
        return {
            "scenario_id": scenario_id,
            "project_id": graph.project_id, "project_mode": mode,
            "SYNTHETIC_TEST_DATA": True,
            "NOT_FOR_CONSTRUCTION": True,
            "project_graph": {"path": str(graph_path)},
            "architecture": {
                "provider": "aias_building_design_core.ArchitecturalProductionCore",
                "path": str(architecture_path) if architecture_path else None,
                "source_graph_sha256": architecture.get("source_graph_sha256") if architecture else None,
                "level_count": len(architecture.get("levels", ())) if architecture else 0,
                "geometry_count": len(architecture.get("geometry_index", {})) if architecture else 0,
            },
            "native_bim": {"path": str(native_bim_path), "wall_count": len(native_bim['walls'])},
            "standards": {"path": str(standards_path), "pack": synthetic_standards_evidence["pack"], "sha256": reinforcement.standards_evidence_sha256, "verdicts": standards_verdicts},
            "reinforcement": {"path": str(reinforcement_path), "bar_set_count": len(reinforcement.bar_sets), "steel_kg": ReinforcementEngine().total_steel_kg(reinforcement), "analysis_evidence_sha256": reinforcement.analysis_evidence_sha256, "standards_evidence_sha256": reinforcement.standards_evidence_sha256, "design_evidence_sha256": reinforcement.design_evidence_sha256, "status": "PRELIMINARY"},
            "drawings": {"model_path": drawing["model_path"], "model_sha256": drawing["model_sha256"], "pdf": drawing["pdf"], "pdf_sha256": drawing["pdf_sha256"], "pdf_file_sha256": drawing["pdf_file_sha256"], "annotation_count": drawing["annotation_count"], "design_trace": drawing["design_trace"], "native_backend": drawing["native_dwg"]["backend"]},
            "structural": {
                "provider": "aias_structural_core.ProjectGraphStructuralAdapter",
                "path": str(structural_path), "sha256": structural_sha256,
                "projection": model.metadata.get("projection"),
                "member_count": len(model.members), "node_count": len(model.nodes),
                "geometry_backed_member_count": model.metadata.get("geometry_backed_member_count", 0),
                "analysis_evidence_sha256": result.evidence_sha256,
                "analysis_model_sha256": result.analysis_trace.get("analysis_model_sha256"),
                "standards_evidence_sha256": result.analysis_trace.get("standards_evidence_sha256"),
                "governing_combination": result.analysis_trace.get("governing_combination"),
                "equilibrium_status": result.analysis_trace.get("equilibrium_status"),
                "status": result.status,
            },
            "coherence": {
                "path": str(coherence_path) if coherence_path else None,
                "verdict": coherence.get("verdict") if coherence else None,
                "checks": coherence.get("checks") if coherence else {},
            },
            "V0_V1": "PASS", "V2": "PASS", "V3": result.status, "V4": "PASS",
            "V5": drawing["gate"], "V6": "PASS" if quantities["gate"] == reports["gate"] == "PASS" else "FAIL",
            "V7": qa["gate"], "V8": issuance["gate"], "quantities": {"reinforcement": quantities["reinforcement"]}, "qa": qa, "issuance": issuance,
            "verdict": issuance["verdict"],
        }

    @staticmethod
    def plan_selective_regeneration(before_manifest: dict, after_manifest: dict) -> dict:
        """Plan downstream invalidation without executing or crossing projects."""
        from aias_project_intake.builders import ParametricProjectGraphBuilder

        builder = ParametricProjectGraphBuilder()
        before = builder.build(before_manifest)
        after = builder.build(after_manifest)
        return ArchitecturalProductionCore().plan_selective_regeneration(before, after)
