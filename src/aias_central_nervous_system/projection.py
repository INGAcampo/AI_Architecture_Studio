"""Deterministic digital-company state projection from CNS event history."""
from __future__ import annotations
class CompanyStateProjection:
 """Reduce delivery, recommendation, risk and credential events into executive state."""
 def __init__(self):self.state={"deliveries":[],"recommendations":[],"risks":[],"credentials_issued":0,"last_sequence":0}
 def apply(self,event:dict)->None:
  """Idempotently apply a supported event according to its global sequence."""
  if event["sequence"]<=self.state["last_sequence"]:return
  kind=event["event_type"]
  if kind=="delivery.completed":self.state["deliveries"].append(event["payload"])
  elif kind=="recommendation.proposed":self.state["recommendations"].append(event["payload"])
  elif kind=="risk.raised":self.state["risks"].append(event["payload"])
  elif kind=="credential.issued":self.state["credentials_issued"]+=1
  self.state["last_sequence"]=event["sequence"]
