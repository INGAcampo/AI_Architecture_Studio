class ConstructivePackValidator:
 def validate(self, pack):
  errors=[]
  for r in pack.get('rules',[]):
   for k in ['rule_id','standard','edition','chapter','section','applicability','inputs','formula_limit','units','verdict_logic','source_document_sha256','evidence_locator']:
    if not r.get(k): errors.append(f"{r.get('rule_id','unknown')} missing {k}")
   if len(r.get('source_document_sha256',''))!=64: errors.append(f"{r.get('rule_id','unknown')} invalid source hash")
  return errors
