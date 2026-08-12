from math import isclose,pi
from aias_structural_codes_program import DeepFoundationEngine,DeepPile,DiaphragmWallCase,EngineeringStudyContext,PileGroupCase,StudySource


def context(status="REFERENCE",pack="",review="PENDING"):
    return EngineeringStudyContext("GEO","R00","BO","SI",(StudySource("G1","GEOTECHNICAL_INVESTIGATION","Lab","evidence://geo",status),),pack,review)


def test_pile_group_capacity_separates_tip_shaft_efficiency_and_safety():
    pile=DeepPile("P1",1,10,1000,50,"G1");case=PileGroupCase("PG",(pile,),.8,500,2.5)
    result=DeepFoundationEngine().pile_group(context(),case)
    expected_tip=1000*pi/4;expected_shaft=50*pi*10
    assert result.status=="PASS_REFERENCE"
    assert isclose(result.pile_capacities[0].tip_capacity_kn,expected_tip)
    assert isclose(result.pile_capacities[0].shaft_capacity_kn,expected_shaft)
    assert isclose(result.ultimate_group_capacity_kn,(expected_tip+expected_shaft)*.8)
    assert result.normative_compliance_claimed is False and result.construction_approved is False


def test_pile_group_exceedance_fails_closed():
    case=PileGroupCase("PG",(DeepPile("P",.5,5,500,20,"G1"),),1,10000,2.5)
    result=DeepFoundationEngine().pile_group(context(),case)
    assert result.status=="REJECTED"
    assert "pile_group_capacity_exceeded" in result.issues


def test_diaphragm_wall_reports_lateral_force_and_base_moment():
    case=DiaphragmWallCase("DW",10,1,.6,20,.3,10,"G1")
    result=DeepFoundationEngine().diaphragm_wall(context(),case)
    assert result.status=="PASS_REFERENCE"
    assert result.lateral_force_kn==330
    assert result.overturning_moment_kn_m==1150


def test_unknown_sources_and_invalid_wall_inputs_are_rejected():
    case=DiaphragmWallCase("DW",-1,1,.6,20,1.2,0,"UNKNOWN")
    result=DeepFoundationEngine().diaphragm_wall(context(),case)
    assert "UNKNOWN:unknown_source_id" in result.issues
    assert "invalid_diaphragm_wall_inputs" in result.issues


def test_authorized_deep_foundation_still_requires_professional_release():
    ctx=context("AUTHORIZED","BO-GEO-002","ACCEPTED");case=PileGroupCase("PG",(DeepPile("P",1,10,1000,50,"G1"),),1,500,2.5)
    result=DeepFoundationEngine().pile_group(ctx,case)
    assert result.status=="PASS_NORMATIVE_REVIEW_REQUIRED"
    assert result.normative_compliance_claimed is True
    assert result.construction_approved is False
