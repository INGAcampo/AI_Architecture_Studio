"""AST-whitelisted declarative calculation execution with golden-thread evidence."""
from __future__ import annotations
import ast,hashlib,json,math
from datetime import datetime,timezone
from aias_aeks.models import KnowledgeUnit
from .admission import KnowledgeAdmission
ALLOWED=(ast.Expression,ast.BinOp,ast.UnaryOp,ast.Add,ast.Sub,ast.Mult,ast.Div,ast.Pow,ast.Mod,ast.USub,ast.UAdd,ast.Name,ast.Load,ast.Constant,ast.Compare,ast.Gt,ast.GtE,ast.Lt,ast.LtE,ast.Eq,ast.NotEq,ast.BoolOp,ast.And,ast.Or)
class DeclarativeKnowledgeExecutor:
 """Execute arithmetic-only knowledge without calls, attributes, imports or mutation."""
 def execute(self,unit:KnowledgeUnit,inputs:dict[str,float],calculation_id:str)->dict:
  """Validate admission, rules and inputs, then return result and integrity evidence."""
  issues=KnowledgeAdmission().validate(unit)
  if issues:raise ValueError("knowledge_not_admitted:"+",".join(issues))
  calculation=next((x for x in unit.calculations if x["calculation_id"]==calculation_id),None)
  if not calculation:raise KeyError(calculation_id)
  if set(inputs)!=(set(calculation["inputs"])):raise ValueError("input_contract_mismatch")
  if any(not isinstance(v,(int,float)) or not math.isfinite(float(v)) for v in inputs.values()):raise ValueError("nonfinite_input")
  for rule in unit.validation_rules:
   if not self._evaluate(rule,inputs):raise ValueError("validation_rule_failed:"+rule)
  value=float(self._evaluate(calculation["expression"],inputs));payload={"eku_id":unit.eku_id,"eku_version":unit.version,"calculation_id":calculation_id,"inputs":dict(inputs),"output":{"name":calculation["output"],"value":value,"unit":calculation["unit"]},"executed_at":datetime.now(timezone.utc).isoformat(),"human_review_required":unit.human_review_required,"jurisdiction":unit.jurisdiction};payload["input_sha256"]=hashlib.sha256(json.dumps(inputs,sort_keys=True,separators=(",",":")).encode()).hexdigest();payload["evidence_sha256"]=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest();return payload
 def _evaluate(self,expression:str,inputs:dict):
  tree=ast.parse(expression,mode="eval")
  if any(not isinstance(node,ALLOWED) for node in ast.walk(tree)):raise ValueError("unsafe_expression")
  if any(isinstance(node,ast.Name) and node.id not in inputs for node in ast.walk(tree)):raise ValueError("unknown_expression_name")
  return eval(compile(tree,"<eku>","eval"),{"__builtins__":{}},dict(inputs))
