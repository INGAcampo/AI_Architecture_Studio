from aias_structural_codes_program import AdapterManifest,GovernedVendorAdapter,VendorExchangeRequest
def request(vendor="ETABS",runtime=True):return VendorExchangeRequest("T1","M1","R1","a"*64,("STATIC_LINEAR",),"SI",AdapterManifest("A1",vendor,"1","22","AIAS-CAE-1",runtime))
def test_supported_vendor_runtime_is_authorized_for_reviewed_execution():
 result=GovernedVendorAdapter().authorize(request());assert result.status=="READY_FOR_VENDOR_EXECUTION" and result.execution_authorized;assert result.professional_review_required and len(result.request_sha256)==64
def test_missing_licensed_runtime_blocks_execution():
 result=GovernedVendorAdapter().authorize(request(runtime=False));assert result.status=="BLOCKED" and "licensed_vendor_runtime_required" in result.issues
def test_unknown_vendor_and_bad_integrity_fail_closed():
 item=request("UNKNOWN");item=VendorExchangeRequest(item.transaction_id,item.model_id,item.model_revision,"bad",item.analysis_types,item.units,item.manifest);issues=GovernedVendorAdapter().authorize(item).issues;assert "unsupported_vendor" in issues and "model_integrity_required" in issues
