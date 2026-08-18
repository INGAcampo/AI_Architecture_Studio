"""Safety, completeness and maturity controls for Project Lighthouse 001."""
REQUIRED=("foundation_plan.svg","foundation_section.svg","bar_schedule.csv","foundation_documentation.json","FOUNDATION_TECHNICAL_REPORT.md")
def validate(files:list[str],brief:dict)->dict:
 """Verify minimum artifacts and enforce reference-only professional boundaries."""
 names={name.rsplit("/",1)[-1] for name in files};missing=[name for name in REQUIRED if name not in names];safe=brief["legal_status"]=="REFERENCE_ONLY" and brief["professional_review_required"] and brief.get("jurisdiction_code")=="VE" and brief.get("normative_compliance_claimed") is False and brief.get("construction_approved") is False
 return {"complete":not missing,"missing":missing,"safe_reference_status":safe,"construction_approved":False,"reference_capability_level":3}
