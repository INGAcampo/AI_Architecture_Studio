from __future__ import annotations
import argparse, ast, hashlib, json, os, platform, re, shutil, subprocess, sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

EXCLUDED_DIRS = {'.git','.venv','venv','env','node_modules','__pycache__','.pytest_cache','.mypy_cache','.ruff_cache','build','dist','AIAS_HANDOFF_CURRENT','AIAS_CHAT_HANDOFF_VERIFY'}
HISTORICAL_HINTS = {'backup','backups','backps','program_packs','programpacks','extractedprograpacks','rar','archives','archive'}
ROOT_MARKERS = ('pyproject.toml','pytest.ini','requirements.txt','.git','src','tests','docs')

@dataclass
class FileRecord:
    path: str; size: int; sha256: str; category: str; extension: str

def now_iso() -> str: return datetime.now(timezone.utc).isoformat()
def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

def category(rel: Path) -> str:
    parts=[p.lower() for p in rel.parts]
    if any(any(h in p for h in HISTORICAL_HINTS) for p in parts): return 'historical_or_packaged'
    if parts and parts[0] in {'src','engineering','sites'}: return 'active_source'
    if parts and parts[0] == 'tests': return 'tests'
    if parts and parts[0] == 'docs': return 'documentation'
    if parts and parts[0].startswith('.aias'): return 'aias_registry'
    if rel.suffix.lower() in {'.toml','.ini','.cfg','.yaml','.yml','.json'}: return 'configuration_or_registry'
    return 'other'

def walk(root: Path) -> Iterable[Path]:
    for dp, dns, fns in os.walk(root):
        dns[:] = [d for d in dns if d not in EXCLUDED_DIRS]
        base=Path(dp)
        for fn in fns:
            p=base/fn
            if p.is_file(): yield p

def module_candidates(root: Path) -> set[str]:
    mods=set()
    for base_name in ('src','engineering'):
        base=root/base_name
        if not base.exists(): continue
        for p in base.rglob('*.py'):
            if any(part in EXCLUDED_DIRS for part in p.parts): continue
            rel=p.relative_to(base)
            parts=list(rel.with_suffix('').parts)
            if parts[-1]=='__init__': parts=parts[:-1]
            if parts: mods.add('.'.join(parts))
    return mods

def import_audit(root: Path):
    mods=module_candidates(root); top={m.split('.')[0] for m in mods}
    unresolved=[]; parse_errors=[]; scanned=0
    for base_name in ('src','engineering'):
        base=root/base_name
        if not base.exists(): continue
        for p in base.rglob('*.py'):
            if any(part in EXCLUDED_DIRS for part in p.parts): continue
            scanned += 1
            try: tree=ast.parse(p.read_text(encoding='utf-8-sig', errors='replace'))
            except SyntaxError as e:
                parse_errors.append({'path':str(p.relative_to(root)),'line':e.lineno,'error':e.msg}); continue
            for n in ast.walk(tree):
                names=[]
                if isinstance(n,ast.Import): names=[a.name for a in n.names]
                elif isinstance(n,ast.ImportFrom) and n.level==0 and n.module: names=[n.module]
                for name in names:
                    head=name.split('.')[0]
                    if head in top and not any(name==m or m.startswith(name+'.') or name.startswith(m+'.') for m in mods):
                        unresolved.append({'path':str(p.relative_to(root)),'line':getattr(n,'lineno',None),'import':name})
    # dedupe
    seen=set(); ded=[]
    for x in unresolved:
        k=(x['path'],x['line'],x['import'])
        if k not in seen: seen.add(k); ded.append(x)
    return {'python_files_scanned':scanned,'candidate_modules':len(mods),'unresolved_internal_imports':ded,'syntax_errors':parse_errors}

def run_cmd(cmd, cwd: Path, timeout=1800):
    try:
        cp=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True,timeout=timeout)
        return {'command':cmd,'returncode':cp.returncode,'stdout':cp.stdout[-120000:],'stderr':cp.stderr[-120000:]}
    except Exception as e: return {'command':cmd,'returncode':-1,'stdout':'','stderr':repr(e)}

def git_state(root: Path):
    if not (root/'.git').exists() or not shutil.which('git'): return {'available':False}
    def g(*a): return run_cmd(['git',*a],root,120)
    return {'available':True,'head':g('rev-parse','HEAD'),'branch':g('branch','--show-current'),'status':g('status','--short'),'log':g('log','-10','--oneline')}

def main():
    ap=argparse.ArgumentParser(description='AIAS Level 2 consolidation truth-baseline auditor')
    ap.add_argument('--root',default='.')
    ap.add_argument('--output',default='AIAS_L2_CONSOLIDATION_CURRENT')
    ap.add_argument('--run-tests',action='store_true')
    ap.add_argument('--test-command',default='python -m pytest -q')
    ap.add_argument('--create-git-tag',action='store_true')
    args=ap.parse_args(); root=Path(args.root).resolve(); out=(root/args.output).resolve()
    if not root.exists(): raise SystemExit(f'Root does not exist: {root}')
    markers={m:(root/m).exists() for m in ROOT_MARKERS}
    if sum(markers.values()) < 2: raise SystemExit('Refusing: selected folder does not look like the AIAS root.')
    out.mkdir(parents=True,exist_ok=True)
    records=[]; groups=defaultdict(list); counts=defaultdict(int); total=0
    for p in walk(root):
        try:
            if out in p.parents: continue
            rel=p.relative_to(root); s=p.stat().st_size; h=sha256(p); c=category(rel)
            records.append(FileRecord(str(rel).replace('\\','/'),s,h,c,p.suffix.lower())); groups[h].append(str(rel).replace('\\','/')); counts[c]+=1; total+=s
        except (OSError,PermissionError): continue
    duplicates=[{'sha256':h,'size':next((r.size for r in records if r.sha256==h),0),'paths':ps} for h,ps in groups.items() if len(ps)>1]
    duplicate_waste=sum(d['size']*(len(d['paths'])-1) for d in duplicates)
    imports=import_audit(root)
    git=git_state(root)
    tests={'executed':False}
    if args.run_tests:
        import shlex
        tests={'executed':True,**run_cmd(shlex.split(args.test_command),root,3600)}
    report={
      'schema':'aias.l2.consolidation.baseline.v1','generated_at':now_iso(),'root':str(root),'environment':{'python':sys.version,'platform':platform.platform()},
      'root_markers':markers,'summary':{'files':len(records),'bytes':total,'categories':dict(counts),'duplicate_groups':len(duplicates),'duplicate_waste_bytes':duplicate_waste,'unresolved_internal_imports':len(imports['unresolved_internal_imports']),'syntax_errors':len(imports['syntax_errors'])},
      'git':git,'imports':imports,'tests':tests,
      'authority_policy':{'active':['src','tests','docs','engineering','sites','project root configuration'],'evidence':['.aias* registries','manifests','roadmaps','handoff'],'non_authoritative':['backups','RAR transport folders','extracted program packs','archives unless explicitly restored']},
      'safety':{'mutated_project_files':False,'deleted_files':False,'merged_backups':False}
    }
    (out/'BASELINE.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
    (out/'COMPONENT_MATRIX.json').write_text(json.dumps([asdict(r) for r in records],indent=2,ensure_ascii=False),encoding='utf-8')
    (out/'DUPLICATES.json').write_text(json.dumps(duplicates,indent=2,ensure_ascii=False),encoding='utf-8')
    (out/'IMPORT_AUDIT.json').write_text(json.dumps(imports,indent=2,ensure_ascii=False),encoding='utf-8')
    md=f'''# AIAS Level 2 Consolidation Baseline\n\nGenerated: {report['generated_at']}\n\n## Summary\n- Files inventoried: **{len(records):,}**\n- Total bytes: **{total:,}**\n- Duplicate groups: **{len(duplicates):,}**\n- Potential duplicate bytes: **{duplicate_waste:,}**\n- Python files scanned: **{imports['python_files_scanned']:,}**\n- Unresolved internal imports: **{len(imports['unresolved_internal_imports']):,}**\n- Syntax errors: **{len(imports['syntax_errors']):,}**\n- Tests executed: **{tests.get('executed',False)}**\n- Test return code: **{tests.get('returncode','N/A')}**\n\n## Authority rule\nThe active source tree is authoritative. Backups, RAR transport folders and extracted Program Packs are evidence/recovery material and are not merged automatically.\n\n## Safety\nThis audit did not delete, overwrite or merge project files.\n'''
    (out/'EXECUTIVE_REPORT.md').write_text(md,encoding='utf-8')
    actions=[]
    if imports['syntax_errors']: actions.append('Resolve syntax errors before integration testing.')
    if imports['unresolved_internal_imports']: actions.append('Review unresolved internal imports; do not auto-create missing modules.')
    if duplicates: actions.append('Review duplicate groups by category; never delete solely by matching hash.')
    if tests.get('executed') and tests.get('returncode')!=0: actions.append('Triage the failing/collection tests from TEST_RESULT.json.')
    if not actions: actions.append('Proceed to L2-BIM-VERTICAL-SLICE-001 after human review of the baseline.')
    (out/'NEXT_ACTIONS.md').write_text('# Next actions\n\n'+'\n'.join(f'{i+1}. {a}' for i,a in enumerate(actions))+'\n',encoding='utf-8')
    (out/'TEST_RESULT.json').write_text(json.dumps(tests,indent=2,ensure_ascii=False),encoding='utf-8')
    # checksums excluding checksum itself
    lines=[]
    for p in sorted(out.iterdir()):
        if p.is_file() and p.name!='checksums.sha256': lines.append(f'{sha256(p)} *{p.name}')
    (out/'checksums.sha256').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    if args.create_git_tag and git.get('available') and tests.get('returncode',1)==0:
        tag='aias-l2-baseline-'+datetime.now().strftime('%Y%m%d-%H%M%S')
        report['git_tag_attempt']=run_cmd(['git','tag','-a',tag,'-m','AIAS L2 consolidation verified baseline'],root,120)
    print(str(out)); return 0
if __name__=='__main__': raise SystemExit(main())
