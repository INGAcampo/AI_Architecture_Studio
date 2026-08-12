from aias_structural_codes_program import AlignmentStation,CivilInfrastructureEngine,CivilSpatialModel,EarthworkSection,EngineeringStudyContext,SpatialReference,StudySource,SurveyPoint,UrbanAsset


def context(status="REFERENCE",pack="",review="PENDING"):
    return EngineeringStudyContext("CIVIL-1","R00","BO","SI",(StudySource("SURVEY","SURVEY","Surveyor","evidence://survey",status),),pack,review)


def model(ctx=None,crs=None):
    return CivilSpatialModel("MODEL-1","R00",ctx or context(),crs or SpatialReference("EPSG",32719,"EGM96"),(SurveyPoint("P1",500000,8100000,100,"SURVEY"),SurveyPoint("P2",500100,8100000,101,"SURVEY"),SurveyPoint("P3",500200,8100000,103,"SURVEY")),(AlignmentStation(0,500000,8100000,100),AlignmentStation(100,500100,8100000,102),AlignmentStation(200,500200,8100000,101)),(EarthworkSection(0,10,2),EarthworkSection(100,20,4),EarthworkSection(200,0,8)),(UrbanAsset("W1","WATER",500010,8100000,99,"SURVEY"),))


def test_civil_model_preserves_crs_and_calculates_corridor_quantities():
    result=CivilInfrastructureEngine().evaluate(model())
    assert result.issues==()
    assert result.crs=="EPSG:32719"
    assert result.alignment_length_m==200
    assert result.maximum_absolute_grade==.02
    assert result.cut_volume_m3==2500
    assert result.fill_volume_m3==900
    assert result.earthwork_balance_m3==1600
    assert result.urban_asset_count==1
    assert len(result.model_sha256)==64
    assert result.construction_approved is False


def test_invalid_crs_and_unknown_survey_source_fail_closed():
    item=model(crs=SpatialReference("UNKNOWN",0,""));points=(SurveyPoint("P1",0,0,0,"MISSING"),SurveyPoint("P2",1,0,0,"MISSING"),SurveyPoint("P3",0,1,0,"MISSING"))
    item=CivilSpatialModel(item.model_id,item.revision,item.context,item.crs,points,item.alignment,item.earthwork_sections,item.urban_assets)
    result=CivilInfrastructureEngine().evaluate(item)
    assert "invalid_horizontal_crs" in result.issues
    assert "vertical_datum_required" in result.issues
    assert any("unknown_source_id" in issue for issue in result.issues)
    assert result.normative_compliance_claimed is False


def test_non_increasing_stations_and_negative_areas_are_rejected():
    item=model();bad_alignment=(item.alignment[0],item.alignment[0]);bad_earthwork=(EarthworkSection(0,1,0),EarthworkSection(0,-1,0))
    item=CivilSpatialModel(item.model_id,item.revision,item.context,item.crs,item.survey_points,bad_alignment,bad_earthwork,item.urban_assets)
    issues=CivilInfrastructureEngine().evaluate(item).issues
    assert "alignment_stations_not_strictly_increasing" in issues
    assert "earthwork_stations_not_strictly_increasing" in issues
    assert any("negative_area" in issue for issue in issues)


def test_normative_claim_requires_authorized_spatial_evidence_pack_and_review():
    result=CivilInfrastructureEngine().evaluate(model(context("AUTHORIZED","BO-ROAD-001","ACCEPTED")))
    assert result.issues==()
    assert result.normative_compliance_claimed is True
    assert result.construction_approved is False


def test_unsupported_urban_asset_type_is_rejected():
    item=model();assets=(UrbanAsset("X","UNKNOWN",0,0,0,"SURVEY"),)
    item=CivilSpatialModel(item.model_id,item.revision,item.context,item.crs,item.survey_points,item.alignment,item.earthwork_sections,assets)
    assert "X:unsupported_asset_type" in CivilInfrastructureEngine().evaluate(item).issues
