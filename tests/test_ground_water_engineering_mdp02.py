from aias_structural_codes_program import CatchmentCase,EngineeringStudyContext,GravityPipeCase,GroundLayer,GroundWaterEngineering,PressurePipeCase,RockShearCase,StudySource


def context(status="REFERENCE",pack="",review="PENDING"):
    return EngineeringStudyContext("STUDY-1","R00","BO","SI",(StudySource("SRC-1","FIELD_AND_REFERENCE","Lab","evidence://source-1",status),),pack,review)


def test_geotechnical_vertical_stress_is_traceable_and_hashed():
    result=GroundWaterEngineering().vertical_stress(context(),"G-1",(GroundLayer("L1",2,18,"SRC-1"),GroundLayer("L2",3,20,"SRC-1")))
    assert result.issues==()
    assert result.values[0]==("vertical_stress",96,"kPa")
    assert len(result.sha256())==64
    assert result.normative_compliance_claimed is False


def test_rock_mechanics_reference_computes_mohr_coulomb_factor():
    result=GroundWaterEngineering().rock_shear(context(),RockShearCase("R-1",20,30,100,50,"SRC-1"))
    values=dict((name,value) for name,value,_ in result.values)
    assert round(values["shear_capacity"],3)==77.735
    assert round(values["factor_of_safety"],3)==1.555


def test_hydrology_and_water_network_calculations_have_explicit_methods_and_units():
    engine=GroundWaterEngineering()
    runoff=engine.rational_peak_flow(context(),CatchmentCase("H-1",10,.7,100,"SRC-1"))
    water=engine.pressure_pipe(context(),PressurePipeCase("W-1",100,.2,.02,130,"SRC-1"))
    sewer=engine.gravity_pipe(context(),GravityPipeCase("S-1",.3,.01,.013,1,"SRC-1"))
    assert round(runoff.values[0][1],3)==1.946
    assert water.method=="HAZEN_WILLIAMS_SI_REFERENCE" and water.values[0][2]=="m/s"
    assert sewer.method=="MANNING_REFERENCE" and sewer.values[0][1]>0


def test_unknown_sources_and_invalid_physical_inputs_fail_closed():
    result=GroundWaterEngineering().pressure_pipe(context(),PressurePipeCase("W",-1,.2,.02,130,"UNKNOWN"))
    assert "unknown_source_id" in result.issues
    assert "invalid_pressure_pipe_inputs" in result.issues
    assert result.normative_compliance_claimed is False


def test_normative_claim_requires_authorized_sources_pack_and_review():
    authorized=context("AUTHORIZED","BO-WATER-001","ACCEPTED")
    result=GroundWaterEngineering().rational_peak_flow(authorized,CatchmentCase("H",1,.5,50,"SRC-1"))
    assert result.issues==()
    assert result.normative_compliance_claimed is True
    assert result.construction_approved is False


def test_draft_or_unreviewed_study_never_claims_normative_compliance():
    result=GroundWaterEngineering().gravity_pipe(context("DRAFT","PACK","PENDING"),GravityPipeCase("S",.3,.01,.013,1,"SRC-1"))
    assert result.normative_compliance_claimed is False
