"""Dashboard status classification without unsupported maturity claims."""
from __future__ import annotations

def maturity_status(reference_level:int,audited_level:int|None)->dict:
 """Separate demonstrated reference capability from audited organization maturity."""
 return {"reference_capability_level":reference_level,"audited_organizational_level":audited_level,"level_5_reference":reference_level==5,"level_5_organizationally_audited":audited_level==5,"warning":None if audited_level==5 else "Nivel 5 organizacional pendiente de medición productiva y auditoría independiente."}

def acceleration_status(reduction:float,classification:str)->dict:
 """Classify sustainable acceleration against the constitutional 45 percent target."""
 return {"time_reduction":reduction,"percent":round(reduction*100,2),"target_percent":45,"meets_target":reduction>=.45,"classification":classification,"audited":classification=="AUDITED_PRODUCTION_MEASUREMENT"}
