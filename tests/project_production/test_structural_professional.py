from aias_building_design_core import BuildingDesignCore
from aias_structural_professional import ProfessionalStructuralEngine

def test_professional_structural_reference_case():
    g=BuildingDesignCore().seed_pilot(BuildingDesignCore().create_project("Pilot")); e=ProfessionalStructuralEngine(); m=e.generate_3d_model(g); e.add_loads(m); e.apply_combinations(m); r=e.analyze_and_design(m,{"pack":"VE-PILOT-001.0"})
    assert r.status == "PASS" and r.design_checks and len(r.evidence_sha256)==64
    assert all("dofs" in n and len(n["dofs"])==6 for n in m.nodes)

def test_professional_fails_closed():
    assert ProfessionalStructuralEngine().analyze_and_design(ProfessionalStructuralEngine().generate_3d_model(BuildingDesignCore().create_project("x")),{}).status == "INSUFFICIENT_EVIDENCE"
