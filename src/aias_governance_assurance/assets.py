"""Stable engineering-asset lifecycle validation."""
import re
STATES={"DRAFT","REVIEW","APPROVED","IMPLEMENTED","VALIDATED","CERTIFIED","DEPRECATED"}
ID=re.compile(r"^[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+$");SEMVER=re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
def validate_asset(asset):
 """Validate stable identifier, semantic version and official state."""
 errors=[]
 if not ID.fullmatch(asset.get("id","")):errors.append("invalid_stable_identifier")
 if not SEMVER.fullmatch(asset.get("version","")):errors.append("invalid_semantic_version")
 if asset.get("status") not in STATES:errors.append("invalid_official_state")
 return errors
