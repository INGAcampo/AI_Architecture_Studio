"""Golden-thread traceability for the Lighthouse technical dossier."""
def golden_thread()->dict:
 """Link the reference need to calculation, drawing, document and review evidence."""
 return {"thread_id":"GT-LIGHTHOUSE-000001","links":[["NEED-001","satisfied_by","REQ-930003"],["REQ-930003","implemented_by","ECP-000001A..F"],["ASSUMPTIONS","constrain","CALCULATION"],["AEKS_REFERENCE","informs","CODE_CHECKS"],["CALCULATION","produces","RESULTS"],["RESULTS","represented_by","DRAWINGS"],["RESULTS","reported_in","TECHNICAL_DOCUMENTS"],["TECHNICAL_DOCUMENTS","requires","PROFESSIONAL_REVIEW"]],"complete":True}
