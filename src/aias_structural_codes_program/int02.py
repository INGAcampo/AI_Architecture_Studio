"""INT-02 governed vendor-adapter envelopes for structural CAE exchange."""
from __future__ import annotations
from dataclasses import asdict,dataclass
import hashlib,json
SUPPORTED_VENDORS={"SAP2000","ETABS","ROBOT"}
@dataclass(frozen=True,slots=True)
class AdapterManifest:
    adapter_id:str;vendor:str;adapter_version:str;vendor_api_version:str;exchange_schema:str;licensed_runtime_available:bool
    def validate(self):
        issues=[]
        if not all((self.adapter_id,self.adapter_version,self.vendor_api_version,self.exchange_schema)):issues.append("adapter_identity_incomplete")
        if self.vendor not in SUPPORTED_VENDORS:issues.append("unsupported_vendor")
        return issues
@dataclass(frozen=True,slots=True)
class VendorExchangeRequest:
    transaction_id:str;model_id:str;model_revision:str;model_sha256:str;analysis_types:tuple[str,...];units:str;manifest:AdapterManifest
    def validate(self):
        issues=self.manifest.validate()
        if not all((self.transaction_id,self.model_id,self.model_revision)):issues.append("exchange_identity_incomplete")
        if len(self.model_sha256)!=64:issues.append("model_integrity_required")
        if self.units!="SI":issues.append("unsupported_exchange_units")
        if not self.analysis_types:issues.append("analysis_types_required")
        return issues
    def digest(self):return hashlib.sha256(json.dumps(asdict(self),sort_keys=True,separators=(",",":")).encode()).hexdigest()
@dataclass(frozen=True,slots=True)
class VendorExchangeDecision:
    transaction_id:str;status:str;request_sha256:str;issues:tuple[str,...];execution_authorized:bool;professional_review_required:bool=True
class GovernedVendorAdapter:
    def authorize(self,request:VendorExchangeRequest)->VendorExchangeDecision:
        issues=request.validate()
        if not request.manifest.licensed_runtime_available:issues.append("licensed_vendor_runtime_required")
        return VendorExchangeDecision(request.transaction_id,"READY_FOR_VENDOR_EXECUTION" if not issues else "BLOCKED",request.digest(),tuple(issues),not issues,True)
