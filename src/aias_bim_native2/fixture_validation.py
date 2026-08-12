from __future__ import annotations
from typing import Any
def validate_fixture(payload: dict[str, Any]) -> dict[str, Any]:
    entities=payload.get("entities",[]); ids=[e.get("id","") for e in entities]; known=set(ids)
    errors=[]
    if len(ids)!=len(set(ids)): errors.append("duplicate_entity_ids")
    for entity in entities:
        if not str(entity.get("ifc_class","")).startswith("Ifc"): errors.append("invalid_ifc_class")
        if any(target not in known for target in entity.get("relationships",[])): errors.append("unknown_relationship_target")
        if any(not isinstance(value,(int,float)) for value in entity.get("properties",{}).values()): errors.append("non_numeric_fixture_property")
    return {"valid":not errors,"entity_count":len(entities),"schema":payload.get("schema"),"errors":sorted(set(errors))}
