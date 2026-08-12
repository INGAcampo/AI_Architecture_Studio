from __future__ import annotations
import argparse, hashlib, json, os, platform, subprocess, sys, zipfile
from datetime import datetime, timezone
from pathlib import Path

EXCLUDE_DIRS={'.git','.venv','venv','node_modules','__pycache__','.pytest_cache','dist','build','backups','RAR','Nueva carpeta'}
TEXT_EXT={'.md','.txt','.json','.toml','.ini','.yaml','.yml','.py','.ps1'}

def run(cmd:list[str], cwd:Path, timeout:int=30)->dict:
    try:
        p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,timeout=timeout)
        return {'command':' '.join(cmd),'returncode':p.returncode,'stdout':p.stdout[-12000:],'stderr':p.stderr[-12000:]}
    except Exception as e:
        return {'command':' '.join(cmd),'returncode':-1,'stdout':'','stderr':repr(e)}

def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def iter_files(root:Path):
    for p in root.rglob('*'):
        if p.is_file() and not any(part in EXCLUDE_DIRS for part in p.relative_to(root).parts):
            yield p

def detect_latest(root:Path)->dict:
    candidates=[]
    for base in [root/'.aias_sprints',root/'docs',root/'logs']:
        if base.exists():
            for p in base.rglob('*'):
                if p.is_file() and p.suffix.lower() in TEXT_EXT:
                    name=p.name.upper()
                    score=0
                    if 'CURRENT' in name or 'STATE' in name: score+=5
                    if 'ROADMAP' in name: score+=4
                    if 'SPRINT' in name or 'CLOSE' in name: score+=3
                    candidates.append((score,p.stat().st_mtime,p))
    candidates.sort(reverse=True)
    return {'candidate_files':[str(p.relative_to(root)) for _,_,p in candidates[:25]]}

def main()->int:
    ap=argparse.ArgumentParser(description='Generate an auditable AIAS cross-chat handoff package.')
    ap.add_argument('--root',default='.',help='AIAS repository root')
    ap.add_argument('--output',default='AIAS_HANDOFF_CURRENT',help='Output directory or absolute path')
    ap.add_argument('--run-tests',action='store_true',help='Run focused pytest collection/smoke check')
    ap.add_argument('--zip',action='store_true',dest='make_zip',help='Create AIAS_CHAT_HANDOFF.zip')
    args=ap.parse_args()
    root=Path(args.root).resolve(); out=Path(args.output); out=(root/out if not out.is_absolute() else out).resolve()
    if not (root/'pyproject.toml').exists() and not (root/'src').exists():
        print(f'ERROR: {root} does not look like the AIAS root.',file=sys.stderr); return 2
    out.mkdir(parents=True,exist_ok=True)
    now=datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')
    git={}
    if (root/'.git').exists():
        git['status']=run(['git','status','--short'],root)
        git['branch']=run(['git','branch','--show-current'],root)
        git['commit']=run(['git','rev-parse','HEAD'],root)
        git['log']=run(['git','log','-10','--oneline','--decorate'],root)
    inventory=[]
    counts={}
    for p in iter_files(root):
        rel=p.relative_to(root).as_posix(); top=rel.split('/')[0]; counts[top]=counts.get(top,0)+1
        if p.stat().st_size<=5_000_000:
            inventory.append({'path':rel,'size':p.stat().st_size,'sha256':sha256(p)})
    tests={}
    if args.run_tests:
        tests['collect']=run([sys.executable,'-m','pytest','--collect-only','-q'],root,120)
    state={
      'schema_version':'1.0.0','protocol':'AIAS-CHAT-HANDOFF-001','generated_at':now,
      'repository_root':str(root),'host':{'platform':platform.platform(),'python':sys.version.split()[0]},
      'root_counts':dict(sorted(counts.items())),'total_hashed_files':len(inventory),
      'continuity_candidates':detect_latest(root),'git':git,'tests':tests,
      'operational_rules':[
        'Treat this package as a snapshot, not as the live repository.',
        'The live repository remains on the user workstation.',
        'Ignore transport-only wrappers named RAR and Nueva carpeta.',
        'Do not declare a sprint complete without source, tests, documentation, and evidence.'
      ]
    }
    (out/'CURRENT_STATE.json').write_text(json.dumps(state,indent=2,ensure_ascii=False),encoding='utf-8')
    (out/'COMPONENT_INVENTORY.json').write_text(json.dumps(inventory,indent=2,ensure_ascii=False),encoding='utf-8')
    summary=f'''# AIAS — Current Handoff\n\nGenerated: {now}\n\n## Authority\nThis package is a portable snapshot for continuity between chats. The active repository remains at the user's local AIAS path.\n\n## Repository evidence\n- Hashed files: {len(inventory)}\n- Root areas: {', '.join(f'{k} ({v})' for k,v in sorted(counts.items()))}\n- Git detected: {'yes' if git else 'no'}\n- Test collection executed: {'yes' if args.run_tests else 'no'}\n\n## Required opening procedure in a new chat\n1. Read `CURRENT_STATE.json`.\n2. Read `EXECUTIVE_SUMMARY.md`, `NEXT_MACRODELIVERY.md`, and `DECISIONS_LOG.md`.\n3. Verify `checksums.sha256`.\n4. Treat claims as provisional until checked against source and tests.\n5. Continue from the recorded next macrodelivery; do not restart completed work.\n'''
    (out/'EXECUTIVE_SUMMARY.md').write_text(summary,encoding='utf-8')
    next_file=out/'NEXT_MACRODELIVERY.md'
    if not next_file.exists(): next_file.write_text('# Next Macrodelivery\n\nUpdate this file before closing every macrodelivery.\n',encoding='utf-8')
    decisions=out/'DECISIONS_LOG.md'
    if not decisions.exists(): decisions.write_text('# Decisions Log\n\n- The local repository is authoritative.\n- Uploaded archives are analysis snapshots only.\n- Ignore transport-only `RAR` and `Nueva carpeta` wrappers.\n',encoding='utf-8')
    (out/'RESTORE_AND_VERIFY.ps1').write_text(r'''param([string]$HandoffPath = $PSScriptRoot)
$ErrorActionPreference = "Stop"
$checksumFile = Join-Path $HandoffPath "checksums.sha256"
if (!(Test-Path $checksumFile)) { throw "checksums.sha256 not found" }
$failed = @()
Get-Content $checksumFile | ForEach-Object {
  if ($_ -match '^([0-9a-f]{64})\s+\*(.+)$') {
    $expected=$matches[1]; $relative=$matches[2]; $file=Join-Path $HandoffPath $relative
    if (!(Test-Path $file) -or (Get-FileHash $file -Algorithm SHA256).Hash.ToLower() -ne $expected) { $failed += $relative }
  }
}
if ($failed.Count) { Write-Host "FAILED:" -ForegroundColor Red; $failed; exit 1 }
Write-Host "AIAS handoff verified successfully." -ForegroundColor Green
''',encoding='utf-8')
    checksum_targets=[p for p in out.rglob('*') if p.is_file() and p.name!='checksums.sha256']
    lines=[f'{sha256(p)} *{p.relative_to(out).as_posix()}' for p in sorted(checksum_targets)]
    (out/'checksums.sha256').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    if args.make_zip:
        z=out.parent/'AIAS_CHAT_HANDOFF.zip'
        with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
            for p in out.rglob('*'):
                if p.is_file(): f.write(p,p.relative_to(out.parent))
        print(z)
    print(out); return 0
if __name__=='__main__': raise SystemExit(main())
