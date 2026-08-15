"""Fast, non-destructive canonical workspace hygiene preflight."""
import json,subprocess,sys
from pathlib import Path
def git(root,*args): return subprocess.check_output(['git','-C',str(root),*args]).decode(errors='replace')
def main():
 root=Path(__file__).resolve().parents[2]; policy=json.loads((root/'engineering/aias/governance/CANONICAL_WORKSPACE_POLICY.json').read_text()); raw=git(root,'ls-files','--others','--exclude-standard','-z').split('\0'); rows=[]; counts={}
 for rel in filter(None,raw):
  p=root/rel; cat='AMBIGUOUS_DO_NOT_TOUCH'
  if any(rel.startswith(x) for x in policy['local_only_prefixes']): cat='LOCAL_RUNTIME_ARTIFACT'
  elif rel.startswith('engineering/aias/') or rel.startswith(('src/','tests/','scripts/','tools/')): cat='CANONICAL_SOURCE_CANDIDATE'
  elif rel.startswith(('AIAS_BACKUP_','ACKC/')): cat='HISTORICAL_COPY_BACKUP'
  counts[cat]=counts.get(cat,0)+1; rows.append({'path':rel,'size':p.stat().st_size if p.exists() and p.is_file() else 0,'mtime':p.stat().st_mtime if p.exists() else None,'classification':cat})
 staged=[x for x in git(root,'diff','--cached','--name-only').splitlines() if x]; tracked=[x for x in git(root,'diff','--name-only').splitlines() if x and x not in policy['protected_drifts']]; candidates=[x for x in rows if x['classification']=='CANONICAL_SOURCE_CANDIDATE']; verdict='CANONICAL_INTEGRATION_SURFACE_READY' if not staged and not tracked and not candidates else 'NOT_READY'
 out={'head':git(root,'rev-parse','HEAD').strip(),'counts':counts,'staged':staged,'tracked_unexpected':tracked,'protected_drifts':policy['protected_drifts'],'untracked':rows,'verdict':verdict}; dest=root/'engineering/aias/governance/WORKTREE_INVENTORY.json'; dest.write_text(json.dumps(out,indent=2)); (dest.with_suffix('.md')).write_text(f"# Workspace inventory\n\nVerdict: `{verdict}`\n\n"+json.dumps(counts,indent=2)); print(json.dumps({'verdict':verdict,'counts':counts},indent=2)); return 0 if verdict=='CANONICAL_INTEGRATION_SURFACE_READY' else 2
if __name__=='__main__': sys.exit(main())
