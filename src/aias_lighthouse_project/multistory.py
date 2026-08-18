"""Deterministic whole-building reference workflow for the Venezuela lighthouse."""
from __future__ import annotations
from dataclasses import asdict

from aias_cad_bim_integration.ifc_sync import NeutralIfcSynchronizer
from aias_cad_bim_integration.models import BimElement, InterchangeModel

from aias_structural_codes_program import (
    AnalysisRequest,
    AnalysisResult,
    BatchMemberDesigner,
    BuildingNode,
    DesignRulePack,
    LoadCase,
    MemberDemand,
    SectionCapacity,
    StructuralBuilding,
    StructuralMember,
    consolidated_report,
)
from aias_structural_codes_program.normative import LoadCombination


def reference_building() -> StructuralBuilding:
    """Return a three-storey, two-bay frame using neutral SI geometry."""
    nodes = tuple(
        BuildingNode(f"N-{level}-{axis}", axis * 5.0, 0.0, level * 3.2)
        for level in range(4)
        for axis in range(3)
    )
    members = []
    for level in range(1, 4):
        for axis in range(3):
            members.append(StructuralMember(f"C-{level}-{axis}", "COLUMN", f"N-{level-1}-{axis}", f"N-{level}-{axis}", "REF-CONCRETE", "UNSIZED"))
        for bay in range(2):
            members.append(StructuralMember(f"B-{level}-{bay}", "BEAM", f"N-{level}-{bay}", f"N-{level}-{bay+1}", "REF-CONCRETE", "UNSIZED"))
    return StructuralBuilding("LIGHTHOUSE-000001", "VE-REF-3S-2B", "R01", "LOCAL_PROJECT_SI", "SI", nodes, tuple(members), "VE-001")


def reference_analysis(building: StructuralBuilding) -> tuple[AnalysisRequest, AnalysisResult]:
    """Produce transparent synthetic demands for pipeline verification, never design approval."""
    cases = (
        LoadCase("D-REF", "DEAD", "Declared reference gravity demand", "AIAS_CONTROLLED_REFERENCE_FIXTURE"),
        LoadCase("L-REF", "LIVE", "Declared reference occupancy demand", "AIAS_CONTROLLED_REFERENCE_FIXTURE"),
        LoadCase("E-REF", "SEISMIC", "Synthetic lateral pipeline demand; not COVENIN", "AIAS_CONTROLLED_REFERENCE_FIXTURE"),
    )
    request = AnalysisRequest("VE-REF-A01", building, cases, "AIAS-REFERENCE-DEMAND-GENERATOR", "1.0.0", ("STATIC_LINEAR",))
    demands = []
    for member in building.members:
        level = int(member.member_id.split("-")[1])
        if member.kind == "COLUMN":
            demands.extend((
                MemberDemand(member.member_id, "D-REF", 300.0 * (4-level), 18.0, 0.0, 0.0, 35.0, 0.0),
                MemberDemand(member.member_id, "E-REF", 80.0, 45.0 * level, 0.0, 0.0, 75.0 * level, 0.0),
            ))
        else:
            demands.extend((
                MemberDemand(member.member_id, "D-REF", 20.0, 70.0, 0.0, 0.0, 145.0, 0.0),
                MemberDemand(member.member_id, "L-REF", 10.0, 55.0, 0.0, 0.0, 110.0, 0.0),
            ))
    return request, AnalysisResult(request.analysis_id, request.solver_id, request.solver_version, "COMPLETED", tuple(demands), ("REFERENCE_DEMANDS_NOT_NORMATIVE_ANALYSIS",))


def execute_reference_design() -> dict:
    """Close the whole-building reference loop through sizing and consolidation."""
    building = reference_building()
    request, analysis = reference_analysis(building)
    pack = DesignRulePack(
        "VE-REFERENCE-CAPACITY-001", "1.0.0", "REFERENCE_ONLY", "VE",
        (
            SectionCapacity("C-300", "COLUMN", 1000.0, 180.0, 220.0, 55.0),
            SectionCapacity("C-400", "COLUMN", 1800.0, 300.0, 400.0, 85.0),
            SectionCapacity("B-250X450", "BEAM", 300.0, 150.0, 230.0, 48.0),
            SectionCapacity("B-300X550", "BEAM", 500.0, 240.0, 420.0, 70.0),
        ),
        "AIAS_CONTROLLED_REFERENCE_FIXTURE_NOT_COVENIN",
    )
    design = BatchMemberDesigner().design(request, analysis, pack)
    report = consolidated_report(request, analysis, design, pack)
    report["jurisdiction"] = "Venezuela"
    report["jurisdiction_profile_id"] = "VE-001"
    report["model_summary"] = {"storeys": 3, "bays": 2, "nodes": len(building.nodes), "members": len(building.members)}
    report["analysis"]["warnings"] = list(analysis.warnings)
    report["reference_load_envelopes"] = reference_combination_envelopes(analysis)
    return report


def reference_combination_envelopes(analysis: AnalysisResult) -> dict:
    """Envelope synthetic combinations without presenting them as Venezuelan rules."""
    combinations = (
        LoadCombination("REF-U1", (("D-REF", 1.2), ("L-REF", 1.6)), "ULTIMATE"),
        LoadCombination("REF-U2", (("D-REF", 1.0), ("E-REF", 1.0)), "SEISMIC"),
        LoadCombination("REF-S1", (("D-REF", 1.0), ("L-REF", 1.0)), "SERVICEABILITY"),
    )
    by_member = {}
    for row in analysis.demands:
        values = by_member.setdefault(row.member_id, {})
        values[row.load_case_id] = {"axial_kn": abs(row.axial_kn), "shear_kn": max(abs(row.shear_y_kn), abs(row.shear_z_kn)), "moment_kn_m": max(abs(row.moment_y_kn_m), abs(row.moment_z_kn_m))}
    envelopes = []
    for member_id, cases in sorted(by_member.items()):
        maxima = {"axial_kn": 0.0, "shear_kn": 0.0, "moment_kn_m": 0.0}
        governing = {key: "" for key in maxima}
        for combination in combinations:
            for response in maxima:
                value = sum(factor * cases.get(case_id, {}).get(response, 0.0) for case_id, factor in combination.factors)
                if value > maxima[response]:
                    maxima[response], governing[response] = value, combination.combination_id
        envelopes.append({"member_id": member_id, "maximum": maxima, "governing_combination": governing})
    return {"legal_status": "REFERENCE_ONLY_NOT_COVENIN", "combinations": [asdict(row) for row in combinations], "member_envelopes": envelopes}


def neutral_bim_ifc_export() -> dict:
    """Create loss-reported IFC 4.3 neutral entities for the complete reference building."""
    elements = []
    for axis in range(3):
        x = axis * 5000.0
        elements.append(BimElement(f"F-{axis}", "Footing", f"Footing {axis}", ((x-700,-700),(x+700,-700),(x+700,700),(x-700,700)), {"level_mm":0,"status":"REFERENCE"}, "LIGHTHOUSE-000001:R01"))
    for level in range(1, 4):
        z = level * 3200
        elements.append(BimElement(f"S-{level}", "Slab", f"Floor slab {level}", ((0,-2000),(10000,-2000),(10000,2000),(0,2000)), {"elevation_mm":z,"thickness_mm":150,"status":"REFERENCE"}, "LIGHTHOUSE-000001:R01"))
        for axis in range(3):
            x = axis * 5000.0
            elements.append(BimElement(f"C-{level}-{axis}", "Column", f"Column {level}-{axis}", ((x-200,-200),(x+200,-200),(x+200,200),(x-200,200)), {"base_elevation_mm":(level-1)*3200,"top_elevation_mm":z,"section":"C-300"}, "LIGHTHOUSE-000001:R01"))
        for bay in range(2):
            x0, x1 = bay * 5000.0, (bay+1) * 5000.0
            elements.append(BimElement(f"B-{level}-{bay}", "Beam", f"Beam {level}-{bay}", ((x0,-150),(x1,-150),(x1,150),(x0,150)), {"elevation_mm":z,"section":"B-250X450"}, "LIGHTHOUSE-000001:R01"))
    model = InterchangeModel("LIGHTHOUSE-VE-BIM-001", "1.0.0", "mm", tuple(elements), {"source":"LIGHTHOUSE-000001:R01","ifc_schema":"IFC4.3","exchange":"NEUTRAL_JSON","jurisdiction_profile":"VE-001"})
    entities, losses = NeutralIfcSynchronizer().export_entities(model)
    return {"schema":"AIAS-IFC4.3-NEUTRAL-EXPORT-1.0","model":model.to_dict(),"ifc_entities":[asdict(row) for row in entities],"losses":list(losses),"native_ifc_file_claimed":False,"professional_review_required":True,"construction_approved":False}
