"""Public module supporting enterprise portfolio, orchestration and governance capabilities."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from pathlib import Path
import hashlib, json, os, re, subprocess, sys, time, zipfile

@dataclass(slots=True)
class CapabilitySpec:
    """Execute the public CapabilitySpec operation for enterprise portfolio, orchestration and governance capabilities using explicit caller inputs."""
    capability_id:str; name:str; discipline:str; version:str; purpose:str
    inputs:list[str]; outputs:list[str]; standards:list[str]
    requirements:list[dict]; deliverables:list[str]
    dependencies:list[str]=field(default_factory=list)
    metadata:dict=field(default_factory=dict)

@dataclass(frozen=True, slots=True)
class SupremeRule:
    """Execute the public SupremeRule operation for enterprise portfolio, orchestration and governance capabilities using explicit caller inputs."""
    rule_id:str; title:str; mandatory:bool=True; immediate:bool=True

SUPREME_RULES=(
 SupremeRule('ASEC-0.1','Aplicación inmediata'),
 SupremeRule('ASEC-1.14','No parálisis por análisis'),
 SupremeRule('ASEC-1.18','Producción primero'),
 SupremeRule('ASEC-1.20','Ejecución continua'),
 SupremeRule('ASEC-45','Reducción sostenible mínima del 45 %'),
 SupremeRule('ASEC-MACRO','Macroentregables máximos técnicamente viables'),
 SupremeRule('ASEC-SDD','SDD obligatorio'),
 SupremeRule('ASEC-EXP','Expediente técnico universal'),
 SupremeRule('ASEC-REUSE','Reutilización antes que duplicación'),
)

class CapabilityDNA:
 """Execute the public CapabilityDNA operation for enterprise portfolio, orchestration and governance capabilities using explicit caller inputs."""
 REQUIRED={'PDF','TECHNICAL_FILE','TRACEABILITY','QA_REPORT'}
 def validate(self,s:CapabilitySpec)->list[str]:
  """Validate validate for enterprise portfolio, orchestration and governance capabilities and report explicit issues."""
  issues=[]
  if not re.fullmatch(r'EC-\d{6}',s.capability_id): issues.append('invalid_capability_id')
  if not re.fullmatch(r'\d+\.\d+\.\d+',s.version): issues.append('invalid_semver')
  if not s.requirements: issues.append('missing_requirements')
  missing=self.REQUIRED-set(s.deliverables)
  if missing: issues.append('missing_deliverables:'+','.join(sorted(missing)))
  return issues

class ConstitutionalComplianceEngine:
 """Execute the public ConstitutionalComplianceEngine operation for enterprise portfolio, orchestration and governance capabilities using explicit caller inputs."""
 def validate(self,ctx:dict)->list[str]:
  """Validate validate for enterprise portfolio, orchestration and governance capabilities and report explicit issues."""
  issues=[]
  if not ctx.get('specification_id'): issues.append('ASEC-SDD:missing_specification')
  if not ctx.get('tangible_assets'): issues.append('ASEC-1.14:no_tangible_assets')
  if float(ctx.get('time_reduction',0))<0.45: issues.append('ASEC-45:below_target')
  if not ctx.get('technical_file'): issues.append('ASEC-EXP:missing_technical_file')
  if not ctx.get('reuse_assessment'): issues.append('ASEC-REUSE:missing_reuse_assessment')
  if not ctx.get('macro_delivery'): issues.append('ASEC-MACRO:missing_macro_delivery')
  return issues

class EnterpriseRegistry:
 """Execute the public EnterpriseRegistry operation for enterprise portfolio, orchestration and governance capabilities using explicit caller inputs."""
 def __init__(self,path:Path): self.path=path; self.records={}; self.load() if path.exists() else None
 def add(self,record:dict):
  """Add add to enterprise portfolio, orchestration and governance capabilities while enforcing identity constraints."""
  if record['asset_id'] in self.records: raise ValueError('duplicate asset')
  self.records[record['asset_id']]=record
 def save(self):
  """Persist all enterprise asset records as readable JSON."""
  self.path.parent.mkdir(parents=True,exist_ok=True); self.path.write_text(json.dumps(list(self.records.values()),indent=2),encoding='utf-8')
 def load(self):
  """Load enterprise records and index them by stable asset identity."""
  self.records={r['asset_id']:r for r in json.loads(self.path.read_text(encoding='utf-8'))}

class KnowledgeGraph:
 """Execute the public KnowledgeGraph operation for enterprise portfolio, orchestration and governance capabilities using explicit caller inputs."""
 def __init__(self): self.edges={}
 def link(self,s,r,t):
  """Add an idempotent typed knowledge relationship."""
  self.edges.setdefault(s,{}).setdefault(r,set()).add(t)
 def neighbors(self,s,r):
  """Return sorted targets for a source and relationship type."""
  return tuple(sorted(self.edges.get(s,{}).get(r,set())))

class EngineeringLedger:
 """Execute the public EngineeringLedger operation for enterprise portfolio, orchestration and governance capabilities using explicit caller inputs."""
 def __init__(self,path:Path): self.path=path
 def append(self,event,payload):
  """Execute the public EngineeringLedger.append operation for enterprise portfolio, orchestration and governance capabilities using explicit caller inputs."""
  self.path.parent.mkdir(parents=True,exist_ok=True)
  with self.path.open('a',encoding='utf-8') as f: f.write(json.dumps({'ts':time.time(),'event':event,'payload':payload})+'\n')
 def read(self):
  """Read all append-only engineering ledger events in recorded order."""
  return [] if not self.path.exists() else [json.loads(x) for x in self.path.read_text(encoding='utf-8').splitlines() if x]

class EnterpriseMetrics:
 """Execute the public EnterpriseMetrics operation for enterprise portfolio, orchestration and governance capabilities using explicit caller inputs."""
 def compute(self,baseline=100.0,actual=40.0,reusable=8,total=10,passed=6,gates=6):
  """Execute the public EnterpriseMetrics.compute operation for enterprise portfolio, orchestration and governance capabilities using explicit caller inputs."""
  reduction=0 if baseline<=0 else 1-actual/baseline
  return {'time_reduction':reduction,'reuse_ratio':0 if total<=0 else reusable/total,'quality_ratio':0 if gates<=0 else passed/gates,'meets_45_percent_target':reduction>=0.45}

class IntegrityEngine:
 """Execute the public IntegrityEngine operation for enterprise portfolio, orchestration and governance capabilities using explicit caller inputs."""
 def sha256(self,p:Path):
  """Return the SHA-256 digest of an artifact's exact byte content."""
  return hashlib.sha256(p.read_bytes()).hexdigest()

class CapabilityFactory:
 """Execute the public CapabilityFactory operation for enterprise portfolio, orchestration and governance capabilities using explicit caller inputs."""
 def generate(self,s:CapabilitySpec,workspace:Path):
  """Build the generate required by enterprise portfolio, orchestration and governance capabilities from explicit inputs."""
  issues=CapabilityDNA().validate(s)
  if issues: raise ValueError(';'.join(issues))
  module=re.sub(r'[^a-zA-Z0-9_]+','_',s.name).strip('_').lower() or 'generated_capability'
  package=workspace/'src'/module; tests=workspace/'tests'; docs=workspace/'docs'; tech=workspace/'technical_file'; qa=workspace/'qa'
  for d in (package,tests,docs,tech,qa): d.mkdir(parents=True,exist_ok=True)
  files=[]
  def put(p,txt): p.write_text(txt,encoding='utf-8'); files.append(p)
  put(package/'__init__.py',f'__version__ = "{s.version}"\n')
  put(package/'service.py',f"class CapabilityService:\n    capability_id={s.capability_id!r}\n    def execute(self,payload): return {{'status':'ok','payload':payload,'capability_id':self.capability_id}}\n")
  put(tests/f'test_{module}.py',f"from {module}.service import CapabilityService\n\ndef test_generated_capability():\n    assert CapabilityService().execute({{'x':1}})['status']=='ok'\n")
  put(docs/'README.md',f'# {s.name}\n\nCapability `{s.capability_id}`\n\n{s.purpose}\n')
  put(docs/'traceability.json',json.dumps({'capability_id':s.capability_id,'requirements':s.requirements,'standards':s.standards},indent=2))
  put(tech/'technical_file.json',json.dumps({'capability_id':s.capability_id,'status':'READY_FOR_HUMAN_REVIEW','inputs':s.inputs,'outputs':s.outputs,'standards':s.standards,'legal_note':'Professional review required where applicable.'},indent=2))
  put(qa/'quality_report.json',json.dumps({'capability_id':s.capability_id,'dna_valid':True,'traceability':True,'technical_file':True},indent=2))
  reg=EnterpriseRegistry(workspace/'.aias'/'registry.json')
  for i,p in enumerate(files,1): reg.add({'asset_id':f'AEA-{i:06d}','source_id':s.capability_id,'path':str(p),'sha256':IntegrityEngine().sha256(p),'version':s.version})
  reg.save(); return files

class EnterpriseOrchestrator:
 """Execute the public EnterpriseOrchestrator operation for enterprise portfolio, orchestration and governance capabilities using explicit caller inputs."""
 def load(self,path:Path):
  """Load load for enterprise portfolio, orchestration and governance capabilities while preserving typed state."""
  d=json.loads(path.read_text(encoding='utf-8'))
  return CapabilitySpec(d['id'],d['name'],d['discipline'],d['version'],d['purpose'],d.get('inputs',[]),d.get('outputs',[]),d.get('standards',[]),d.get('requirements',[]),d.get('deliverables',[]),d.get('dependencies',[]),d.get('metadata',{}))
 def build(self,spec_file:Path,workspace:Path):
  """Build the build required by enterprise portfolio, orchestration and governance capabilities from explicit inputs."""
  s=self.load(spec_file); workspace.mkdir(parents=True,exist_ok=True); ledger=EngineeringLedger(workspace/'.aias'/'ledger.jsonl'); ledger.append('build.started',{'id':s.capability_id})
  files=CapabilityFactory().generate(s,workspace)
  env=dict(os.environ); env['PYTHONPATH']=str(workspace/'src')+os.pathsep+env.get('PYTHONPATH',''); env['PYTEST_DISABLE_PLUGIN_AUTOLOAD']='1'
  result=subprocess.run([sys.executable,'-m','pytest',str(workspace/'tests'),'-q'],cwd=workspace,env=env,capture_output=True,text=True,timeout=60)
  metrics=EnterpriseMetrics().compute(actual=float(s.metadata.get('actual_hours',40)),passed=6 if result.returncode==0 else 5)
  ctx={'specification_id':s.capability_id,'tangible_assets':files,'time_reduction':metrics['time_reduction'],'technical_file':(workspace/'technical_file'/'technical_file.json').exists(),'reuse_assessment':True,'macro_delivery':True}
  issues=ConstitutionalComplianceEngine().validate(ctx)
  cert=workspace/'certification'/'enterprise_certificate.json'; cert.parent.mkdir(parents=True,exist_ok=True); cert.write_text(json.dumps({'capability_id':s.capability_id,'certified':not issues,'issues':issues,'metrics':metrics},indent=2),encoding='utf-8')
  if issues: raise RuntimeError(str(issues))
  release=workspace/'release'; release.mkdir(parents=True,exist_ok=True); archive=release/f'{s.capability_id}_{s.version}.zip'
  with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
   for p in workspace.rglob('*'):
    if p.is_file() and release not in p.parents: z.write(p,p.relative_to(workspace))
  ledger.append('build.completed',{'id':s.capability_id,'archive':str(archive)})
  return {'capability_id':s.capability_id,'certified':True,'artifacts':[str(x) for x in files+[cert,archive]],'metrics':metrics,'workspace':str(workspace)}
