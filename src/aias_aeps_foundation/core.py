"""Public module supporting the AEPS foundation production runtime."""
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime, timezone
import json, re
from pathlib import Path
class Status(str,Enum):
 """Execute the public Status operation for the AEPS foundation production runtime using explicit caller inputs."""
 DRAFT='DRAFT'; REVIEW='REVIEW'; APPROVED='APPROVED'; IMPLEMENTED='IMPLEMENTED'; VALIDATED='VALIDATED'; CERTIFIED='CERTIFIED'; RELEASED='RELEASED'; DEPRECATED='DEPRECATED'; ARCHIVED='ARCHIVED'
class Relation(str,Enum):
 """Execute the public Relation operation for the AEPS foundation production runtime using explicit caller inputs."""
 IMPLEMENTS='implements'; DEPENDS_ON='depends_on'; EXTENDS='extends'; REQUIRES='requires'; REFERENCES='references'; GENERATES='generates'; VALIDATES='validates'; TESTS='tests'; CERTIFIES='certifies'; CONTAINS='contains'; SUPERSEDES='supersedes'; REPLACES='replaces'
PREFIXES={'AEPS','AEO','AEKM','AEC','ASDD','ARCH','ADR','REQ','SPEC','RULE','STD','PROC','TEST','VAL','GEN','PACK','REL','KPI','OBJ'}
PAT=re.compile(r'^(?P<p>[A-Z]+)-(?P<n>\d{6})$')
SEMVER=re.compile(r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$')
@dataclass(frozen=True,slots=True)
class Link:
 """Typed relationship from one engineering asset to a stable target identity."""
 relation:Relation; target_id:str; description:str=''
@dataclass(slots=True)
class Asset:
 """Execute the public Asset operation for the AEPS foundation production runtime using explicit caller inputs."""
 asset_id:str; title:str; asset_type:str; version:str; status:Status; owner:str; purpose:str; scope:str
 dependencies:list[str]=field(default_factory=list); relationships:list[Link]=field(default_factory=list); requirements:list[str]=field(default_factory=list); validations:list[str]=field(default_factory=list); metrics:dict=field(default_factory=dict); history:list[dict]=field(default_factory=list)
 created_at:str=field(default_factory=lambda:datetime.now(timezone.utc).isoformat()); updated_at:str=field(default_factory=lambda:datetime.now(timezone.utc).isoformat())
 def touch(self,note):
  """Update modification time and append an immutable lifecycle note."""
  self.updated_at=datetime.now(timezone.utc).isoformat(); self.history.append({'timestamp':self.updated_at,'note':note})
class IdentifierRegistry:
 """Execute the public IdentifierRegistry operation for the AEPS foundation production runtime using explicit caller inputs."""
 def __init__(self): self.used=set()
 def valid(self,x):
  """Execute the public IdentifierRegistry.valid operation for the AEPS foundation production runtime using explicit caller inputs."""
  m=PAT.fullmatch(x); return bool(m and m.group('p') in PREFIXES)
 def register(self,x):
  """Add register to the AEPS foundation production runtime while enforcing identity constraints."""
  if not self.valid(x): raise ValueError(x)
  if x in self.used: raise ValueError('duplicate')
  self.used.add(x)
 def next(self,prefix):
  """Execute the public IdentifierRegistry.next operation for the AEPS foundation production runtime using explicit caller inputs."""
  if prefix not in PREFIXES: raise ValueError(prefix)
  nums=[int(x.split('-')[1]) for x in self.used if x.startswith(prefix+'-')]; x=f'{prefix}-{max(nums,default=0)+1:06d}'; self.register(x); return x
class Validator:
 """Execute the public Validator operation for the AEPS foundation production runtime using explicit caller inputs."""
 def validate(self,a,known=None):
  """Validate validate for the AEPS foundation production runtime and report explicit issues."""
  e=[]
  if not IdentifierRegistry().valid(a.asset_id): e.append('invalid_id')
  if not SEMVER.fullmatch(a.version): e.append('invalid_version')
  for k in ('title','asset_type','owner','purpose','scope'):
   if not getattr(a,k,'').strip(): e.append('missing_'+k)
  if known is not None:
   for d in a.dependencies:
    if d not in known: e.append('unknown_dependency')
   for r in a.relationships:
    if r.target_id not in known: e.append('unknown_relation')
  return e
class Generator:
 """Execute the public Generator operation for the AEPS foundation production runtime using explicit caller inputs."""
 def __init__(self): self.ids=IdentifierRegistry()
 def create(self,prefix,title,asset_type,owner,purpose,scope):
  """Build the create required by the AEPS foundation production runtime from explicit inputs."""
  a=Asset(self.ids.next(prefix),title,asset_type,'0.1.0',Status.DRAFT,owner,purpose,scope); a.touch('Created by GEN-000001'); return a
 def save(self,a,path):
  """Persist save for the AEPS foundation production runtime in its stable external representation."""
  d=asdict(a); d['status']=a.status.value; d['relationships']=[{'relation':x.relation.value,'target_id':x.target_id,'description':x.description} for x in a.relationships]; Path(path).parent.mkdir(parents=True,exist_ok=True); Path(path).write_text(json.dumps(d,indent=2),encoding='utf-8')
class Registry:
 """Execute the public Registry operation for the AEPS foundation production runtime using explicit caller inputs."""
 def __init__(self): self.assets={}
 def add(self,a):
  """Add add to the AEPS foundation production runtime while enforcing identity constraints."""
  if a.asset_id in self.assets: raise ValueError('duplicate')
  if Validator().validate(a,set(self.assets)|{a.asset_id}): raise ValueError('invalid')
  self.assets[a.asset_id]=a
class Metrics:
 """Calculate safe AEPS production ratios from measured numerator and denominator values."""
 @staticmethod
 def ratio(a,b):
  """Return a safe ratio, using zero when the denominator is nonpositive."""
  return 0.0 if b<=0 else a/b
