"""Machine-verifiable Charter, Handbook and component-contract controls."""
from __future__ import annotations
class FoundationValidator:
 """Validate institutional documents and architecture dependency contracts."""
 def validate_charter(self,charter:dict)->list[str]:
  """Validate identity, mission, targets, authority and professional boundaries."""
  errors=[]
  for key in ("id","version","status","identity","mission","strategic_targets","professional_boundary","authority"):
   if not charter.get(key):errors.append(f"missing_charter:{key}")
  if charter.get("strategic_targets",{}).get("minimum_sustainable_time_reduction",0)<.45:errors.append("acceleration_target_below_constitution")
  if "licensed_professional_role" not in charter.get("professional_boundary",{}):errors.append("missing_professional_boundary")
  return errors
 def validate_handbook(self,handbook:dict)->list[str]:
  """Validate layer uniqueness, dependency direction and contract requirements."""
  errors=[];layers=handbook.get("layers",[]);ids=[x.get("id") for x in layers]
  if len(ids)!=len(set(ids)):errors.append("duplicate_layers")
  rank={item:i for i,item in enumerate(ids)}
  for layer in layers:
   for dependency in layer.get("may_depend_on",[]):
    if dependency not in rank:errors.append(f"unknown_layer:{dependency}")
    elif rank[dependency]>=rank[layer["id"]]:errors.append(f"forbidden_dependency:{layer['id']}->{dependency}")
  if len(handbook.get("component_contract_required_fields",[]))<9:errors.append("incomplete_component_contract")
  return errors
 def validate_component(self,component:dict,handbook:dict)->list[str]:
  """Validate required public-contract fields and allowed architectural dependencies."""
  errors=[f"missing_contract:{key}" for key in handbook["component_contract_required_fields"] if key not in component];layers={x["id"]:set(x["may_depend_on"]) for x in handbook["layers"]};layer=component.get("layer")
  if layer not in layers:return errors+["unknown_component_layer"]
  for dependency in component.get("dependency_layers",[]):
   if dependency not in layers[layer]:errors.append(f"forbidden_dependency:{layer}->{dependency}")
  return errors
