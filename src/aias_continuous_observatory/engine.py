"""Continuous observation cycle, deduplication, scoring, radar and recommendation ledger."""
from __future__ import annotations
import json,os,tempfile
from datetime import datetime,timezone,timedelta
from pathlib import Path
from .models import FeedItem
from .registry import SourceRegistry
from aias_technology_observatory.scoring import score
class ContinuousObservatory:
 """Run deterministic, injectable ATO cycles without coupling tests to the network."""
 def __init__(self,registry:SourceRegistry,ledger_path:Path):self.registry=registry;self.path=ledger_path;self.ledger=self._load()
 def _load(self):
  if not self.path.exists():return {"schema_version":"1.0.0","observations":{},"cycles":[],"recommendations":[]}
  return json.loads(self.path.read_text(encoding="utf-8"))
 def due_sources(self,now:datetime)->tuple[str,...]:
  """Return sources whose configured cadence has elapsed since their last cycle."""
  latest={}
  for cycle in self.ledger["cycles"]:latest.update(cycle.get("source_times",{}))
  due=[]
  for sid,source in self.registry.sources.items():
   previous=datetime.fromisoformat(latest[sid]) if sid in latest else None
   if previous is None or now-previous>=timedelta(hours=source["cadence_hours"]):due.append(sid)
  return tuple(sorted(due))
 def run_cycle(self,fetcher,now:datetime|None=None)->dict:
  """Fetch due authorized sources, admit new items and emit actionable AEC-000050 recommendations."""
  now=now or datetime.now(timezone.utc);admitted=[];duplicates=0;source_times={}
  for sid in self.due_sources(now):
   source=self.registry.sources[sid];items=fetcher(source)
   source_times[sid]=now.isoformat()
   for item in items:
    if item.source_id!=sid:raise ValueError("source_identity_mismatch")
    self.registry.authorize(sid,item.url);fp=item.fingerprint()
    if fp in self.ledger["observations"]:duplicates+=1;continue
    result=score(item.relevance,item.impact,item.reuse,item.acceleration,item.risk,source["evidence_strength"])
    row={**item.to_dict(),"score":result,"observed_at":now.isoformat(),"source":source};self.ledger["observations"][fp]=row;admitted.append(row)
    if result["giant_step"]:self.ledger["recommendations"].append(self._recommendation(row))
  cycle={"cycle_id":f"ATO-CYCLE-{len(self.ledger['cycles'])+1:06d}","completed_at":now.isoformat(),"sources_checked":len(source_times),"admitted":len(admitted),"duplicates":duplicates,"source_times":source_times}
  self.ledger["cycles"].append(cycle);self._save();return {**cycle,"radar":self.radar(),"new_recommendations":sum(x["observation_fingerprint"] in {a["fingerprint"] for a in admitted} for x in self.ledger["recommendations"])}
 def _recommendation(self,row):
  """Build the complete evidence, benefit, tradeoff, risk, action and urgency contract."""
  return {"recommendation_id":f"REC-{row['fingerprint'][:12].upper()}","observation":row["title"],"observation_fingerprint":row["fingerprint"],"evidence":{"publisher":row["source"]["publisher"],"url":row["url"],"strength":row["source"]["evidence_strength"]},"expected_benefit":f"Evaluate {row['domain']} opportunity scoring {row['score']['score']}/100.","cost_and_tradeoffs":"Requires bounded technical spike, integration review and maintenance ownership.","risk":row["score"]["dimensions"]["risk"],"recommended_action":"Open an SDD-governed technology-admission spike with an immediate real consumer.","urgency":"HIGH" if row["score"]["score"]>=75 else "MEDIUM","status":"PROPOSED"}
 def radar(self)->dict:
  """Classify admitted observations into adopt, trial, assess and hold radar rings."""
  rings={"ADOPT":[],"TRIAL":[],"ASSESS":[],"HOLD":[]}
  for row in self.ledger["observations"].values():
   value=row["score"]["score"];ring="ADOPT" if value>=80 else "TRIAL" if value>=65 else "ASSESS" if value>=45 else "HOLD";rings[ring].append(row["fingerprint"])
  return {k:sorted(v) for k,v in rings.items()}
 def _save(self):
  """Atomically persist the observation, cycle and recommendation ledger."""
  self.path.parent.mkdir(parents=True,exist_ok=True);fd,name=tempfile.mkstemp(dir=self.path.parent,suffix=".tmp")
  try:
   with os.fdopen(fd,"w",encoding="utf-8") as stream:json.dump(self.ledger,stream,ensure_ascii=False,indent=2);stream.write("\n")
   os.replace(name,self.path)
  finally:
   if os.path.exists(name):os.unlink(name)
