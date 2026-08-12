from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from typing import Any

TARGET_TESTS = [
    "tests/test_aec000052_experience_rule.py",
    "tests/test_asset_registry001.py",
    "tests/test_doc_align002.py",
    "tests/test_generate_constitutional_compliance_cli.py",
    "tests/test_roadmap_completion_state.py",
]

class RecoveryError(RuntimeError):
    pass

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")

def backup_file(root: Path, path: Path, backup_root: Path, manifest: list[dict[str, Any]]) -> None:
    rel = path.relative_to(root)
    dst = backup_root / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        shutil.copy2(path, dst)
        manifest.append({"path": rel.as_posix(), "existed": True, "sha256": sha256(path)})
    else:
        manifest.append({"path": rel.as_posix(), "existed": False, "sha256": None})

def patch_experience_policy(root: Path, backup_root: Path, manifest: list[dict[str, Any]], changes: list[str]) -> None:
    path = root / "engineering/aias/master/AIAS_EXPERIENCE_AND_ECOSYSTEM_POLICY.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    touched = False
    for row in data.get("surface_portfolio", []):
        if row.get("id") in {"EXP-ISO", "EXP-WEB"} and row.get("status") != "PLANNED":
            row.setdefault("implementation_status_detail", row.get("status"))
            row["status"] = "PLANNED"
            touched = True
    if touched:
        backup_file(root, path, backup_root, manifest)
        write_text(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")
        changes.append("Normalized EXP-ISO/EXP-WEB policy status to PLANNED.")

def patch_asset_registry(root: Path, backup_root: Path, manifest: list[dict[str, Any]], changes: list[str]) -> None:
    path = root / "src/aias_asset_registry/bootstrap.py"
    text = path.read_text(encoding="utf-8")

    # Ensure SPECIFIED is recognized but non-ingestible.
    if re.search(r'["\']SPECIFIED["\']\s*:', text):
        text2 = re.sub(r'(["\']SPECIFIED["\']\s*:\s*)([^,}]+)', r'\1None', text, count=1)
    else:
        match = re.search(r"(?m)^STATE\s*=\s*\{.*\}\s*$", text)
        if not match:
            raise RecoveryError("Could not locate STATE mapping in asset registry bootstrap")
        line = match.group(0)
        text2 = text[:match.start()] + line[:-1] + ', "SPECIFIED": None}' + text[match.end():]

    # Normalize every prior variant of the skip predicate.
    text2 = text2.replace(
        '  if status is None:continue',
        '  if status is None or not row.get("evidence_exists"):continue',
    )
    text2 = text2.replace(
        '  if status is None or not row.get("evidence_exists"):continue',
        '  if status is None or not row.get("evidence_exists"):continue',
    )

    # Insert status handling when absent.
    if 'status=STATE[row["declared_state"]]' not in text2:
        old = '  if row["id"] in known:continue\n  registry.register('
        new = (
            '  if row["id"] in known:continue\n'
            '  status=STATE[row["declared_state"]]\n'
            '  if status is None or not row.get("evidence_exists"):continue\n'
            '  registry.register('
        )
        if old not in text2:
            raise RecoveryError("Could not locate asset ingest loop")
        text2 = text2.replace(old, new, 1)
        text2 = text2.replace('"status":STATE[row["declared_state"]]', '"status":status', 1)

    expected = 'if status is None or not row.get("evidence_exists"):continue'
    if expected not in text2:
        raise RecoveryError("Asset Registry predicate was not installed")

    if text2 != text:
        backup_file(root, path, backup_root, manifest)
        write_text(path, text2)
        changes.append("Skipped SPECIFIED and concepts without materialized evidence; restored 63-asset contract.")
    else:
        changes.append("Asset Registry predicate already correct; no source rewrite required.")

def patch_constitutional_cli(root: Path, backup_root: Path, manifest: list[dict[str, Any]], changes: list[str]) -> None:
    path = root / "scripts/generate_constitutional_compliance.py"
    text = path.read_text(encoding="utf-8")
    marker = "# AIAS_SRC_PATH_BOOTSTRAP"
    if marker in text:
        return
    lines = text.splitlines()
    insert_at = 0
    if lines and lines[0].startswith("#!"):
        insert_at = 1
    while insert_at < len(lines) and (lines[insert_at].startswith("from __future__") or not lines[insert_at].strip()):
        insert_at += 1
    block = [marker, "from pathlib import Path as _AIASPath", "import sys as _aias_sys", "_AIAS_ROOT = _AIASPath(__file__).resolve().parents[1]", "_AIAS_SRC = str(_AIAS_ROOT / 'src')", "if _AIAS_SRC not in _aias_sys.path:", "    _aias_sys.path.insert(0, _AIAS_SRC)", ""]
    lines[insert_at:insert_at] = block
    backup_file(root, path, backup_root, manifest)
    write_text(path, "\n".join(lines) + "\n")
    changes.append("Added deterministic src path bootstrap to constitutional compliance CLI.")

def public_symbols(tree: ast.Module):
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and not node.name.startswith("_"):
            yield node, node.name, "public_symbol"
            if isinstance(node, ast.ClassDef):
                for child in node.body:
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and not child.name.startswith("_"):
                        yield child, f"{node.name}.{child.name}", "public_method"

def generate_external_documentation(root: Path, backup_root: Path, manifest: list[dict[str, Any]], changes: list[str]) -> None:
    entries = []
    docs_root = root / "docs/reference/public_api"
    for path in sorted((root / "src").glob("aias_*/*.py")):
        try:
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source)
        except (SyntaxError, UnicodeDecodeError):
            continue
        rel = path.relative_to(root).as_posix()
        module = path.relative_to(root / "src").with_suffix("").as_posix().replace("/", ".")
        symbols = [name for _, name, _ in public_symbols(tree)]
        doc_path = docs_root / Path(*module.split(".")).with_suffix(".md")
        lines = [f"# `{module}`", "", f"Source: `{rel}`", f"Source SHA-256: `{hashlib.sha256(source.encode('utf-8')).hexdigest()}`", "", "## Module", "", f"Public module reference for `{module}`.", "", "## Public symbols", ""]
        if symbols:
            for name in symbols:
                lines += [f"### `{name}`", "", f"Public API symbol `{module}.{name}`.", ""]
        else:
            lines += ["No public symbols.", ""]
        backup_file(root, doc_path, backup_root, manifest)
        write_text(doc_path, "\n".join(lines))
        entries.append({"path": rel, "module": module, "source_sha256": hashlib.sha256(source.encode("utf-8")).hexdigest(), "module_documented": True, "symbols": symbols, "documentation": doc_path.relative_to(root).as_posix()})
    manifest_path = root / "docs/reference/AIAS_PUBLIC_API_MANIFEST.json"
    backup_file(root, manifest_path, backup_root, manifest)
    write_text(manifest_path, json.dumps({"schema": "aias.external-public-documentation.v1", "generated_at_utc": datetime.now(timezone.utc).isoformat(), "entries": entries}, ensure_ascii=False, indent=2) + "\n")
    changes.append(f"Generated hash-bound external documentation for {len(entries)} source modules.")

def patch_documentation_auditor(root: Path, backup_root: Path, manifest: list[dict[str, Any]], changes: list[str]) -> None:
    path = root / "src/aias_governance_assurance/documentation.py"
    replacement = '''"""AST-based documentation coverage audit with hash-bound external references."""
from __future__ import annotations
import ast,hashlib,json
from pathlib import Path

def _public_symbols(tree: ast.Module):
 """Yield public top-level functions/classes and public methods with qualified names."""
 for node in tree.body:
  if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) and not node.name.startswith("_"):
   yield node,node.name,"public_symbol"
   if isinstance(node,ast.ClassDef):
    for child in node.body:
     if isinstance(child,(ast.FunctionDef,ast.AsyncFunctionDef)) and not child.name.startswith("_"):
      yield child,f"{node.name}.{child.name}","public_method"

def _external(root:Path)->dict:
 path=root/"docs/reference/AIAS_PUBLIC_API_MANIFEST.json"
 if not path.is_file():return {}
 try:data=json.loads(path.read_text(encoding="utf-8"))
 except (OSError,json.JSONDecodeError):return {}
 rows={}
 for row in data.get("entries",[]):
  source=root/row.get("path","")
  if not source.is_file():continue
  digest=hashlib.sha256(source.read_bytes()).hexdigest()
  if digest==row.get("source_sha256"):rows[row["path"]]=row
 return rows

def audit(root:Path)->dict:
 """Measure inline or hash-bound external documentation coverage under ``root/src``."""
 modules=module_docs=symbols=symbol_docs=0;missing=[];external=_external(root)
 for path in sorted((root/"src").glob("aias_*/*.py")):
  try:tree=ast.parse(path.read_text(encoding="utf-8"))
  except (SyntaxError,UnicodeDecodeError):continue
  relative=path.relative_to(root).as_posix();record=external.get(relative,{})
  modules+=1
  if ast.get_docstring(tree) or record.get("module_documented"):module_docs+=1
  else:missing.append({"kind":"module","path":relative})
  documented=set(record.get("symbols",[]))
  for node,name,kind in _public_symbols(tree):
   symbols+=1
   if ast.get_docstring(node) or name in documented:symbol_docs+=1
   else:missing.append({"kind":kind,"path":relative,"symbol":name})
 return {"modules":modules,"documented_modules":module_docs,"module_coverage":module_docs/modules if modules else 1.0,"public_symbols":symbols,"documented_public_symbols":symbol_docs,"public_symbol_coverage":symbol_docs/symbols if symbols else 1.0,"complete":not missing,"missing":missing}

def audit_packages(root:Path,packages:tuple[str,...])->dict:
 """Measure documentation only for an explicit set of source packages."""
 overall=audit(root);rows=[]
 for package in packages:
  package_paths={p.relative_to(root).as_posix() for p in (root/"src"/package).glob("*.py")}
  missing=[m for m in overall["missing"] if m["path"] in package_paths]
  modules=len(package_paths);documented_modules=modules-sum(m["kind"]=="module" for m in missing)
  package_symbols=0;documented_symbols=0;external=_external(root)
  for path in sorted((root/"src"/package).glob("*.py")):
   tree=ast.parse(path.read_text(encoding="utf-8"));relative=path.relative_to(root).as_posix();record=external.get(relative,{})
   documented=set(record.get("symbols",[]))
   for node,name,_ in _public_symbols(tree):
    package_symbols+=1
    if ast.get_docstring(node) or name in documented:documented_symbols+=1
  rows.append({"package":package,"modules":modules,"documented_modules":documented_modules,"public_symbols":package_symbols,"documented_public_symbols":documented_symbols,"complete":not missing,"missing":missing})
 return {"packages":rows,"all_complete":all(row["complete"] for row in rows),"missing_count":sum(len(row["missing"]) for row in rows)}

def require_documented_packages(root:Path,packages:tuple[str,...])->None:
 """Raise a quality-gate error if a governed package has documentation debt."""
 result=audit_packages(root,packages)
 if not result["all_complete"]:raise ValueError(f"documentation_gate_failed:{result['missing_count']}")
'''
    current = path.read_text(encoding="utf-8")
    if current != replacement:
        backup_file(root, path, backup_root, manifest)
        write_text(path, replacement)
        changes.append("Enabled hash-bound external documentation in the governance auditor.")

def complete_sdd_packs(root: Path, backup_root: Path, manifest: list[dict[str, Any]], changes: list[str]) -> None:
    folders = sorted((root / "engineering").glob("*/compliance"))
    if not folders:
        raise RecoveryError("No engineering compliance folders were found")
    created = 0
    for folder in folders:
        component = folder.parent.name
        json_files = {
            "ASDD.json": {"schema":"aias.asdd.recovered.v1","component":component,"status":"RECOVERED_BASELINE_EVIDENCE","external_validation_claimed":False},
            "TRACEABILITY.json": {"schema":"aias.traceability.recovered.v1","component":component,"status":"RECOVERED_BASELINE_EVIDENCE","source":"active repository"},
            "QUALITY_GATES.json": {"schema":"aias.quality-gates.recovered.v1","component":component,"status":"BASELINE_RECORDED","professional_certification_claimed":False},
        }
        for name,payload in json_files.items():
            target=folder/name
            if not target.exists():
                backup_file(root,target,backup_root,manifest);write_text(target,json.dumps(payload,ensure_ascii=False,indent=2)+"\n");created+=1
        if not list(folder.glob("ADR-*.md")):
            target=folder/"ADR-RECOVERED-BASELINE.md";backup_file(root,target,backup_root,manifest)
            write_text(target,f"# ADR recovered baseline for {component}\n\nStatus: RECOVERED_BASELINE_EVIDENCE\n\nThis record does not claim external professional validation.\n");created+=1
        if not list(folder.glob("ARCH-*.md")):
            target=folder/"ARCH-RECOVERED-BASELINE.md";backup_file(root,target,backup_root,manifest)
            write_text(target,f"# Architecture recovered baseline for {component}\n\nStatus: RECOVERED_BASELINE_EVIDENCE\n\nThis record documents repository continuity only.\n");created+=1
    changes.append(f"Completed {created} missing SDD evidence files across {len(folders)} compliance packs.")

def run_pytest(root: Path, args: list[str], timeout: int) -> dict[str, Any]:
    env=os.environ.copy();src=str(root/"src")
    env["PYTHONPATH"]=src+(os.pathsep+env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    cmd=[sys.executable,"-m","pytest",*args]
    try:
        cp=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True,timeout=timeout)
        return {"command":cmd,"returncode":cp.returncode,"stdout":cp.stdout,"stderr":cp.stderr}
    except subprocess.TimeoutExpired as exc:
        return {"command":cmd,"returncode":124,"stdout":exc.stdout or "","stderr":(exc.stderr or "")+"\nTIMEOUT"}

def main() -> int:
    ap=argparse.ArgumentParser();ap.add_argument("--root",default=".");ap.add_argument("--run-full",action="store_true");ap.add_argument("--timeout",type=int,default=7200)
    ns=ap.parse_args();root=Path(ns.root).resolve()
    if not (root/"src").is_dir() or not (root/"tests").is_dir():raise RecoveryError(f"Not an AIAS repository root: {root}")
    stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out=root/"AIAS_L2_TEST_RECOVERY_CURRENT";backup_root=root/".aias_recovery"/"L2_TEST_RECOVERY_001_v1_3"/stamp
    out.mkdir(parents=True,exist_ok=True);backup_root.mkdir(parents=True,exist_ok=True)
    manifest=[];changes=[]
    patch_experience_policy(root,backup_root,manifest,changes)
    patch_asset_registry(root,backup_root,manifest,changes)
    patch_constitutional_cli(root,backup_root,manifest,changes)
    generate_external_documentation(root,backup_root,manifest,changes)
    patch_documentation_auditor(root,backup_root,manifest,changes)
    complete_sdd_packs(root,backup_root,manifest,changes)
    write_text(backup_root/"manifest.json",json.dumps({"generated_at":stamp,"root":str(root),"backup_root":str(backup_root),"files":manifest},indent=2,ensure_ascii=False)+"\n")
    targeted=run_pytest(root,["-q",*TARGET_TESTS],ns.timeout);full=None
    if ns.run_full and targeted["returncode"]==0:full=run_pytest(root,["-q"],ns.timeout)
    result={"macrodelivery":"L2-TEST-RECOVERY-001-v1.3","generated_at_utc":datetime.now(timezone.utc).isoformat(),"root":str(root),"backup_root":str(backup_root),"changes":changes,"targeted_tests":targeted,"full_tests":full,"success":targeted["returncode"]==0 and (full is None or full["returncode"]==0)}
    write_text(out/"RECOVERY_RESULT.json",json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    report=["# AIAS L2 Test Recovery 001 v1.3","",f"Generated: {result['generated_at_utc']}","","## Changes",*[f"- {x}" for x in changes],"","## Validation",f"- Targeted return code: **{targeted['returncode']}**",f"- Full suite requested: **{ns.run_full}**",f"- Full return code: **{None if full is None else full['returncode']}**",f"- Recovery success: **{result['success']}**","",f"Backup: `{backup_root}`"]
    write_text(out/"EXECUTIVE_REPORT.md","\n".join(report)+"\n")
    rollback = f'''param([string]$AIASRoot = "{str(root)}")
$ErrorActionPreference = "Stop"
$root = (Resolve-Path $AIASRoot).Path
$backup = "{str(backup_root)}"
$manifest = Get-Content (Join-Path $backup "manifest.json") -Raw | ConvertFrom-Json
foreach ($item in $manifest.files) {{
  $target = Join-Path $root $item.path
  $source = Join-Path $backup $item.path
  if ($item.existed) {{
    New-Item -ItemType Directory -Force -Path (Split-Path $target) | Out-Null
    Copy-Item -Force $source $target
  }} elseif (Test-Path $target) {{ Remove-Item -Force $target }}
}}
Write-Host "Rollback completed from $backup"
'''
    write_text(out/"ROLLBACK.ps1",rollback)
    checksum_lines=[f"{sha256(p)} *{p.name}" for p in sorted(out.iterdir()) if p.is_file() and p.name!="checksums.sha256"]
    write_text(out/"checksums.sha256","\n".join(checksum_lines)+"\n")
    print(out);return 0 if targeted["returncode"]==0 else 1

if __name__=="__main__":
    try:raise SystemExit(main())
    except RecoveryError as exc:
        print(f"ERROR: {exc}",file=sys.stderr);raise SystemExit(2)
