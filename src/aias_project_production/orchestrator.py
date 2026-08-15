from pathlib import Path

from aias_building_design_core.core import BuildingDesignCore
from aias_structural_professional.engine import ProfessionalStructuralEngine

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

    def run(self, scenario_id: str) -> dict:
        if scenario_id not in {"BEST_CASE_001", "NOMINAL_CASE_001", "STRESS_CASE_001"}:
            raise ValueError("unknown synthetic scenario")
        scenario_dir = self.output_root / scenario_id
        core = BuildingDesignCore()
        graph = core.seed_pilot(core.create_project(f"Synthetic {scenario_id}"))
        errors = core.validate(graph)
        if errors:
            return {"verdict": "BLOCKED_SOFTWARE", "errors": errors}
        structural = ProfessionalStructuralEngine()
        model = structural.generate_3d_model(graph)
        structural.add_loads(model)
        if scenario_id == "STRESS_CASE_001":
            for load in model.loads:
                load["magnitude"] *= 30.0
        structural.apply_combinations(model)
        result = structural.analyze_and_design(model, {"synthetic_test_data": True, "scenario_id": scenario_id})
        drawing = self.drawing.produce(graph, result, scenario_dir / "drawings")
        quantities = self.quantities.produce(graph, scenario_dir / "quantities")
        reports = self.reports.produce(graph, result, drawing["model"], quantities["package"], scenario_dir / "reports")
        qa = self.qa.evaluate(result, drawing, quantities, reports, scenario_id)
        issuance = self.issuance.issue(scenario_id, scenario_dir, drawing, quantities, reports, qa)
        return {
            "scenario_id": scenario_id,
            "SYNTHETIC_TEST_DATA": True,
            "NOT_FOR_CONSTRUCTION": True,
            "V0_V1": "PASS", "V2": "PASS", "V3": result.status, "V4": "PASS",
            "V5": drawing["gate"], "V6": "PASS" if quantities["gate"] == reports["gate"] == "PASS" else "FAIL",
            "V7": qa["gate"], "V8": issuance["gate"], "qa": qa, "issuance": issuance,
            "verdict": issuance["verdict"],
        }
