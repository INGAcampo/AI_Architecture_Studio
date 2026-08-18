"""Portfolio item scoring, dependency selection and evidence-gated stage transitions."""
from __future__ import annotations
from dataclasses import dataclass,field,asdict
import json
from pathlib import Path
@dataclass(slots=True)
class PortfolioItem:
 """Governed macro-delivery candidate with value, risk, effort and evidence state."""
 item_id:str;title:str;dependencies:list[str]=field(default_factory=list);stage:str="PROPOSED";strategic_value:float=.5;urgency:float=.5;reuse:float=.5;acceleration:float=.5;compliance:float=.5;risk:float=.5;effort:float=.5;evidence:dict=field(default_factory=dict);benefits:dict=field(default_factory=dict)
 def to_dict(self)->dict:
  """Serialize the complete portfolio record for persistence and Dashboard use."""
  return asdict(self)
class PortfolioOffice:
 """Prioritize dependency-ready work and prohibit unsupported stage claims."""
 def __init__(self,policy_path:Path):self.policy=json.loads(policy_path.read_text(encoding="utf-8"));self.items={}
 def add(self,item:PortfolioItem)->None:
  """Add a uniquely identified item after validating normalized scoring dimensions."""
  if item.item_id in self.items:raise ValueError("duplicate_portfolio_item")
  values=(item.strategic_value,item.urgency,item.reuse,item.acceleration,item.compliance,item.risk,item.effort)
  if any(not 0<=x<=1 for x in values):raise ValueError("portfolio_dimensions_out_of_range")
  self.items[item.item_id]=item
 def score(self,item:PortfolioItem)->float:
  """Return the policy-weighted value score after risk and effort penalties."""
  w=self.policy["priority_weights"];value=w["strategic_value"]*item.strategic_value+w["urgency"]*item.urgency+w["reuse"]*item.reuse+w["acceleration"]*item.acceleration+w["compliance"]*item.compliance-w["risk_penalty"]*item.risk-w["effort_penalty"]*item.effort;return round(100*max(0,value),2)
 def select_next(self,completed:set[str])->PortfolioItem|None:
  """Select the highest-scoring proposed item whose dependencies are complete."""
  candidates=[x for x in self.items.values() if x.stage=="PROPOSED" and set(x.dependencies)<=completed];return max(candidates,key=lambda x:(self.score(x),x.item_id),default=None)
 def transition(self,item_id:str,target:str,evidence:dict)->PortfolioItem:
  """Advance exactly one policy stage only when all target-gate evidence is present."""
  item=self.items[item_id];stages=self.policy["stages"]
  if target not in stages or stages.index(target)!=stages.index(item.stage)+1:raise ValueError("invalid_portfolio_transition")
  merged={**item.evidence,**evidence};missing=[x for x in self.policy["required_gate_evidence"].get(target,[]) if not merged.get(x)]
  if missing:raise ValueError("missing_gate_evidence:"+",".join(missing))
  item.evidence=merged;item.stage=target;return item
 def measure_benefit(self,item_id:str,baseline_hours:float,actual_hours:float,classification:str)->dict:
  """Measure time reduction with explicit evidence classification and target status."""
  if baseline_hours<=0 or actual_hours<0:raise ValueError("invalid_benefit_hours")
  reduction=1-actual_hours/baseline_hours;result={"baseline_hours":baseline_hours,"actual_hours":actual_hours,"time_reduction":reduction,"classification":classification,"meets_45_percent_target":reduction>=self.policy["constitutional_target_time_reduction"]};self.items[item_id].benefits=result;return result
