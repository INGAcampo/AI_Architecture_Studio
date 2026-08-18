"""INT-03 governed AutoCAD, Revit and Civil 3D transaction contracts."""
from __future__ import annotations
from dataclasses import asdict,dataclass
import hashlib,json
REQUIRED_CONTENT={"AUTOCAD":{"DRAWINGS","LAYERS","UNITS"},"REVIT":{"BIM_ELEMENTS","LEVELS","PARAMETERS"},"CIVIL3D":{"SURFACES","ALIGNMENTS","CORRIDORS","CRS"}}
@dataclass(frozen=True,slots=True)
class DesignApplicationManifest:
    adapter_id:str;application:str;adapter_version:str;application_api_version:str;licensed_runtime_available:bool
@dataclass(frozen=True,slots=True)
class DesignExchangeTransaction:
    transaction_id:str;model_id:str;revision:str;source_sha256:str;units:str;content:tuple[str,...];coordinate_reference:str;manifest:DesignApplicationManifest
    def validate(self):
        issues=[];required=REQUIRED_CONTENT.get(self.manifest.application)
        if not all((self.transaction_id,self.model_id,self.revision,self.manifest.adapter_id,self.manifest.adapter_version,self.manifest.application_api_version)):issues.append("transaction_identity_incomplete")
        if required is None:issues.append("unsupported_design_application")
        else:
            missing=required-set(self.content)
            if missing:issues.append(f"missing_exchange_content:{sorted(missing)}")
        if len(self.source_sha256)!=64:issues.append("source_integrity_required")
        if self.units not in {"mm","m"}:issues.append("unsupported_units")
        if self.manifest.application=="CIVIL3D" and not self.coordinate_reference:issues.append("civil3d_crs_required")
        return issues
    def sha256(self):return hashlib.sha256(json.dumps(asdict(self),sort_keys=True,separators=(",",":")).encode()).hexdigest()
@dataclass(frozen=True,slots=True)
class DesignExchangeDecision:
    transaction_id:str;status:str;issues:tuple[str,...];transaction_sha256:str;commit_required:bool=True;professional_review_required:bool=True
class GovernedDesignApplicationAdapter:
    def authorize(self,transaction:DesignExchangeTransaction):
        issues=transaction.validate()
        if not transaction.manifest.licensed_runtime_available:issues.append("licensed_application_runtime_required")
        return DesignExchangeDecision(transaction.transaction_id,"READY_FOR_APPLICATION_EXECUTION" if not issues else "BLOCKED",tuple(issues),transaction.sha256())
