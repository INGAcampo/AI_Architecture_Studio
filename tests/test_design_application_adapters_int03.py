from aias_cad_bim_integration import DesignApplicationManifest,DesignExchangeTransaction,GovernedDesignApplicationAdapter,REQUIRED_CONTENT
def transaction(app="REVIT",runtime=True,content=None,crs=""):
 m=DesignApplicationManifest("A1",app,"1","2026",runtime);return DesignExchangeTransaction("T1","M1","R1","a"*64,"mm",tuple(content or REQUIRED_CONTENT.get(app,())),crs,m)
def test_all_three_vendor_contracts_can_reach_execution_gate():
 for app in ("AUTOCAD","REVIT","CIVIL3D"):
  result=GovernedDesignApplicationAdapter().authorize(transaction(app,crs="EPSG:32719"));assert result.status=="READY_FOR_APPLICATION_EXECUTION" and result.commit_required and result.professional_review_required
def test_vendor_runtime_is_mandatory():
 result=GovernedDesignApplicationAdapter().authorize(transaction(runtime=False));assert result.status=="BLOCKED" and "licensed_application_runtime_required" in result.issues
def test_civil3d_requires_crs_and_complete_civil_content():
 result=GovernedDesignApplicationAdapter().authorize(transaction("CIVIL3D",content=("SURFACES",)));assert "civil3d_crs_required" in result.issues and any(x.startswith("missing_exchange_content") for x in result.issues)
def test_unknown_application_and_bad_hash_fail_closed():
 item=transaction("UNKNOWN");item=DesignExchangeTransaction(item.transaction_id,item.model_id,item.revision,"bad",item.units,item.content,item.coordinate_reference,item.manifest);issues=GovernedDesignApplicationAdapter().authorize(item).issues;assert "unsupported_design_application" in issues and "source_integrity_required" in issues
