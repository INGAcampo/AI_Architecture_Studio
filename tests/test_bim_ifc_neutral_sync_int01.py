from aias_cad_bim_integration import BimElement,IfcNeutralEntity,InterchangeModel,NeutralIfcSynchronizer


def bim(value=30,extra=()):
    wall=BimElement("GID-1","Wall","W1",((0,0),(1000,0),(1000,200),(0,200)),{"strength":value,"locked":"x"},"model://source")
    return InterchangeModel("M1","1","mm",(wall,)+extra,{"source":"model"})


def test_ifc43_neutral_import_preserves_global_identity_and_reports_losses():
    rows=(IfcNeutralEntity("GID-1","IfcWall","W",((0,0),(1,0),(1,1)),{"strength":30},"ifc://1"),IfcNeutralEntity("GID-X","IfcProxy","X",((0,0),(1,0),(1,1)),{},"ifc://2"))
    model,losses=NeutralIfcSynchronizer().import_entities("M1","1",rows,"ifc://file")
    assert model.elements[0].element_id=="GID-1"
    assert model.provenance["ifc_schema"]=="IFC4.3"
    assert losses==({"global_id":"GID-X","reason":"unsupported_ifc_kind","kind":"IfcProxy"},)


def test_neutral_export_maps_supported_types_without_claiming_native_file():
    rows,losses=NeutralIfcSynchronizer().export_entities(bim())
    assert rows[0].kind=="IfcWall" and rows[0].global_id=="GID-1"
    assert losses==()


def test_three_way_sync_returns_change_set_requiring_commit():
    result=NeutralIfcSynchronizer().synchronize(bim(30),bim(35),bim(30),{"strength"})
    assert result.changes[0]["source"]=="AIAS"
    assert result.conflicts==()
    assert result.requires_transaction_commit and result.professional_review_required
    assert len(result.baseline_sha256)==64


def test_divergent_changes_are_conflicts_not_silent_overwrites():
    result=NeutralIfcSynchronizer().synchronize(bim(30),bim(35),bim(40),{"strength"})
    assert result.changes==()
    assert result.conflicts[0]["aias"]==35 and result.conflicts[0]["ifc"]==40


def test_non_allowlisted_changes_and_missing_identity_are_losses():
    missing=InterchangeModel("M1","1","mm",(),{"source":"ifc"});result=NeutralIfcSynchronizer().synchronize(bim(),bim(),missing,{"strength"})
    assert any(x["reason"]=="identity_not_present_in_all_models" for x in result.losses)
