from aias_structural_codes_program import EngineeringStudyContext,InterfaceDisplacement,SoilSpring,SoilStructureInteractionEngine,SoilStructureRequest,StudySource


def context(status="REFERENCE",pack="",review="PENDING"):
    return EngineeringStudyContext("GEO","R00","BO","SI",(StudySource("G1","GEOTECHNICAL_INVESTIGATION","Lab","evidence://geo",status),),pack,review)


def request(ctx=None,displacement=.01):
    return SoilStructureRequest("SSI-1","structural://model","geotech://model",ctx or context(),(SoilSpring("S1","N1","Z",10000,150,"G1"),),(InterfaceDisplacement("N1","Z",displacement,"SERVICE"),))


def test_ssi_elastic_reaction_is_traceable_and_not_construction_approved():
    result=SoilStructureInteractionEngine().analyze(request())
    assert result.status=="COMPLETED" and result.issues==()
    assert result.reactions[0].reaction_kn==100
    assert result.reactions[0].yielded is False
    assert result.maximum_utilization==2/3
    assert len(result.request_sha256)==64
    assert result.normative_compliance_claimed is False
    assert result.construction_approved is False


def test_ssi_caps_reaction_at_ultimate_and_reports_yielding():
    result=SoilStructureInteractionEngine().analyze(request(displacement=-.02))
    assert result.reactions[0].reaction_kn==-150
    assert result.reactions[0].yielded is True
    assert result.reactions[0].secant_stiffness_kn_m==7500


def test_missing_interface_spring_fails_closed():
    item=request();item=SoilStructureRequest(item.analysis_id,item.structural_model_reference,item.geotechnical_model_reference,item.context,item.springs,(InterfaceDisplacement("N2","Z",.01,"SERVICE"),))
    result=SoilStructureInteractionEngine().analyze(item)
    assert result.status=="REJECTED"
    assert result.unmatched_interfaces==("N2:Z:SERVICE",)
    assert any("spring_missing" in issue for issue in result.issues)


def test_invalid_spring_source_and_properties_are_rejected():
    item=request();bad=(SoilSpring("S","N1","BAD",-1,0,"UNKNOWN"),);item=SoilStructureRequest(item.analysis_id,item.structural_model_reference,item.geotechnical_model_reference,item.context,bad,item.displacements)
    issues=SoilStructureInteractionEngine().analyze(item).issues
    assert "S:invalid_direction" in issues
    assert "S:invalid_spring_properties" in issues
    assert "S:unknown_source_id" in issues


def test_normative_ssi_claim_requires_authorized_geotechnical_evidence():
    result=SoilStructureInteractionEngine().analyze(request(context("AUTHORIZED","BO-GEO-001","ACCEPTED")))
    assert result.status=="COMPLETED"
    assert result.normative_compliance_claimed is True
    assert result.construction_approved is False
