"""Executable reference workflow joining SDD, traceability, gates and productivity."""
from pathlib import Path
import json
from .generators import RequirementGenerator, SpecificationGenerator
from .models import RequirementStatus
from .traceability import TraceabilityMatrix
from .quality import QualityGateEngine
from .kpi import ProductivitySnapshot
from .constitution import FOUNDATIONAL_ARTICLES

def run_foundation_demo(output_dir: Path) -> dict:
    """Generate a fully linked specification and persist its constitutional evidence."""
    output_dir.mkdir(parents=True, exist_ok=True)
    rg = RequirementGenerator()
    sg = SpecificationGenerator()
    req = rg.create(
        1,
        "Generate engineering assets",
        "The system shall generate traceable engineering assets.",
        "Eliminate repetitive manual setup."
    )
    req.status = RequirementStatus.APPROVED
    req.acceptance_criteria = ["Generated asset has a valid identifier.", "Generated asset passes validation."]
    req.implements = ["GEN-000001"]
    req.tested_by = ["TEST-000001"]
    spec = sg.create(
        1,
        "AEPS Generation Specification",
        "Define generation of traceable engineering assets.",
        "AEPS Development Platform."
    )
    spec.requirements.append(req)
    spec.architecture_refs.append("ARCH-000001")
    spec.adr_refs.append("ADR-000001")

    matrix = TraceabilityMatrix()
    matrix.link(req.requirement_id, "implemented_by", "GEN-000001")
    matrix.link(req.requirement_id, "tested_by", "TEST-000001")

    gates = QualityGateEngine().evaluate(spec, matrix)
    kpi = ProductivitySnapshot(100.0, 50.0, 30.0, 8, 10)

    result = {
        "specification": spec.specification_id,
        "quality_gates": [{"id": g.gate_id, "passed": g.passed, "message": g.message} for g in gates],
        "time_reduction": kpi.time_reduction,
        "meets_45_percent_target": kpi.meets_acceleration_target,
        "constitutional_articles": [a.article_id for a in FOUNDATIONAL_ARTICLES],
    }
    path = output_dir / "aeps_governance_sdd_demo.json"
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    result["output"] = str(path)
    return result
