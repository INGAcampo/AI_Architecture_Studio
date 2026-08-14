"""Controlled, read-only AutoCAD Core Console reopen inspection isolation."""
from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUTOCAD = Path(r"C:\Program Files\Autodesk\AutoCAD 2027\accoreconsole.exe")
BASE = ROOT / "engineering/aias/dependency_resolution/DR-01A_R1_VALID_DXF_WRITER"
DWG = BASE / "output/roundtrip/A-101.dwg"
OUT = BASE / "output/r2"


def cad_path(path: Path) -> str:
    return str(path.resolve()).replace("\\", "/")


def run(name: str, script: str, timeout: int = 45) -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    script_path = OUT / f"{name}.scr"
    script_path.write_text(script, encoding="ascii")
    started = time.time()
    process = subprocess.Popen(
        [str(AUTOCAD), "/i", str(DWG), "/s", str(script_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        stdout, stderr = process.communicate(timeout=timeout)
        timed_out = False
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        timed_out = True
    finished = time.time()
    return {
        "pid": process.pid,
        "started_epoch": started,
        "finished_epoch": finished,
        "duration_seconds": round(finished - started, 3),
        "timeout_seconds": timeout,
        "timed_out": timed_out,
        "exit_code": process.returncode,
        "stdout_tail": stdout[-4000:],
        "stderr_tail": stderr[-4000:],
        "script": script_path.name,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sentinel = OUT / "REOPEN_SENTINEL.txt"
    inspection = OUT / "REOPEN_INSPECTION.txt"
    sentinel.unlink(missing_ok=True)
    inspection.unlink(missing_ok=True)
    sentinel_script = (
        f'(setq f (open "{cad_path(sentinel)}" "w"))\n'
        '(write-line (strcat "DWGNAME|" (getvar "DWGNAME")) f)\n'
        '(write-line (strcat "ACADVER|" (getvar "ACADVER")) f)\n'
        '(close f)\n(princ)\n_.QUIT\n'
    )
    result = {"drawing": DWG.name, "backend": str(AUTOCAD), "sentinel": run("sentinel", sentinel_script)}
    result["sentinel"]["exists"] = sentinel.exists()
    result["sentinel"]["content"] = sentinel.read_text(encoding="utf-8", errors="replace") if sentinel.exists() else ""
    if not (result["sentinel"]["exit_code"] == 0 and sentinel.exists() and not result["sentinel"]["timed_out"]):
        result["verdict"] = "BLOCKER_REOPEN_SENTINEL_TIMEOUT_OR_FAILURE"
    else:
        inspect_script = (
            f'(setq f (open "{cad_path(inspection)}" "w"))\n'
            '(setq e (entnext) n 0)\n'
            '(while e (setq d (entget e)) (write-line (strcat "ENTITY|" (cdr (assoc 0 d)) "|" (if (assoc 8 d) (cdr (assoc 8 d)) "") "|" (cdr (assoc 5 d))) f) (setq n (+ n 1)) (setq e (entnext e)))\n'
            '(write-line (strcat "COUNT|" (itoa n)) f)\n'
            '(close f)\n(princ)\n_.QUIT\n'
        )
        result["inspection"] = run("inspection", inspect_script)
        lines = inspection.read_text(encoding="utf-8", errors="replace").splitlines() if inspection.exists() else []
        entities = [line.split("|") for line in lines if line.startswith("ENTITY|")]
        result["inspection"].update({
            "exists": inspection.exists(),
            "entity_count": len(entities),
            "types": sorted({row[1] for row in entities if len(row) > 1}),
            "layers": sorted({row[2] for row in entities if len(row) > 2 and row[2]}),
            "handles": [row[3] for row in entities if len(row) > 3],
        })
        result["verdict"] = "REOPEN_INSPECTION_PASS" if result["inspection"]["exit_code"] == 0 and inspection.exists() and not result["inspection"]["timed_out"] else "BLOCKER_INSPECTOR_EXECUTION_LOGIC"
    (OUT / "DR01AR2_REOPEN_ISOLATION.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
