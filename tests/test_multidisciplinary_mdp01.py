from datetime import date
from aias_structural_codes_program import CodeCheckRule,DomainAction,DomainDesignRequest,DomainResistance,GovernedDomainDesigner,MaterialCodePack,NormativeSource,REQUIRED_COVERAGE,StructuralCodePack


def pack(domain):
    source=NormativeSource("REF","Reference dataset","1","AIAS","REFERENCE","internal://reference")
    parent=StructuralCodePack("REF-PARENT","1","GENERIC",date(2026,1,1),None,"REFERENCE_ONLY",(source,),(),None)
    rules=tuple(CodeCheckRule(f"R-{category}",category,"REF",f"section:{category}",f"impl:{category}",f"test:{category}","SI") for category in REQUIRED_COVERAGE[domain])
    return MaterialCodePack(f"REF-{domain}","1",domain,parent,rules,("benchmark:reference",),"ACCEPTED")


def request(domain,system,soil=""):
    return DomainDesignRequest("D1","O1",domain,system,"geometry://1","material://1","analysis://1",(DomainAction("AXIAL",400,"kN"),DomainAction("FLEXURE",80,"kNm")),(DomainResistance("AXIAL",500,"kN","R-AXIAL"),DomainResistance("FLEXURE",100,"kNm","R-FLEXURE")),soil)


def test_mdp01_defines_complete_coverage_for_three_new_domains():
    assert {"TIMBER","MASONRY","ADVANCED_FOUNDATION"}<=set(REQUIRED_COVERAGE)
    assert all(pack(domain).validate()==[] for domain in ("TIMBER","MASONRY","ADVANCED_FOUNDATION"))


def test_timber_and_masonry_reference_designs_are_transparent_and_not_construction_approved():
    for domain,system in (("TIMBER","BEAM"),("MASONRY","SHEAR_WALL")):
        result=GovernedDomainDesigner().design(request(domain,system),pack(domain),"GENERIC",date(2026,8,3))
        assert result.status=="PASS_REFERENCE"
        assert result.governing_utilization==.8
        assert result.normative_compliance_claimed is False
        assert result.construction_approved is False


def test_advanced_foundation_requires_traceable_soil_model():
    result=GovernedDomainDesigner().design(request("ADVANCED_FOUNDATION","PILE"),pack("ADVANCED_FOUNDATION"),"GENERIC",date(2026,8,3))
    assert result.status=="REJECTED"
    assert "soil_model_reference_required" in result.issues


def test_advanced_foundation_calculates_governing_ratio_with_soil_provenance():
    result=GovernedDomainDesigner().design(request("ADVANCED_FOUNDATION","PILE","geotech://model-1"),pack("ADVANCED_FOUNDATION"),"GENERIC",date(2026,8,3))
    assert result.status=="PASS_REFERENCE"
    assert result.governing_check_id=="AXIAL"


def test_capacity_exceedance_and_unit_mismatch_fail_closed():
    item=request("TIMBER","BEAM")
    bad=DomainDesignRequest(item.design_id,item.object_id,item.domain,item.system_type,item.geometry_reference,item.material_reference,item.analysis_reference,(DomainAction("AXIAL",600,"kN"),),(DomainResistance("AXIAL",500,"N","R"),))
    result=GovernedDomainDesigner().design(bad,pack("TIMBER"),"GENERIC",date(2026,8,3))
    assert result.status=="REJECTED"
    assert "AXIAL:unit_mismatch" in result.issues
