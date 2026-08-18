"""COORD-01 executive and multidisciplinary coordination dashboard."""
from __future__ import annotations
from dataclasses import asdict,dataclass
import hashlib,html,json
from pathlib import Path

REQUIRED_DISCIPLINES={"STRUCTURAL","BIM","GEOTECHNICAL","HYDRAULIC","CIVIL"}
@dataclass(frozen=True,slots=True)
class DisciplineStatus:
    discipline:str;model_id:str;revision:str;evidence_sha256:str;status:str;open_issues:int
@dataclass(frozen=True,slots=True)
class CoordinationInterface:
    interface_id:str;source_discipline:str;target_discipline:str;status:str;evidence_locator:str
@dataclass(frozen=True,slots=True)
class CoordinationIssue:
    issue_id:str;discipline:str;severity:str;status:str;description:str;evidence_locator:str
@dataclass(frozen=True,slots=True)
class CoordinationSnapshot:
    project_id:str;revision:str;disciplines:tuple[DisciplineStatus,...];interfaces:tuple[CoordinationInterface,...];issues:tuple[CoordinationIssue,...];release_readiness:str;blocking_reasons:tuple[str,...];snapshot_sha256:str;professional_release_required:bool=True
class CoordinationDashboardEngine:
    def build(self,project_id,revision,disciplines,interfaces,issues):
        blockers=[];names=[x.discipline for x in disciplines];missing=sorted(REQUIRED_DISCIPLINES-set(names))
        if not project_id or not revision:blockers.append("project_identity_incomplete")
        if missing:blockers.append(f"missing_disciplines:{missing}")
        if len(names)!=len(set(names)):blockers.append("duplicate_discipline")
        for row in disciplines:
            if not all((row.model_id,row.revision)) or len(row.evidence_sha256)!=64:blockers.append(f"{row.discipline}:invalid_evidence")
            if row.status not in {"VALIDATED","WARNING","BLOCKED"} or row.status=="BLOCKED":blockers.append(f"{row.discipline}:not_ready")
        for row in interfaces:
            if row.source_discipline not in names or row.target_discipline not in names or not row.evidence_locator:blockers.append(f"{row.interface_id}:invalid_interface")
            if row.status!="RESOLVED":blockers.append(f"{row.interface_id}:unresolved_interface")
        for row in issues:
            if row.severity not in {"LOW","MEDIUM","HIGH","CRITICAL"}:blockers.append(f"{row.issue_id}:invalid_severity")
            if row.severity=="CRITICAL" and row.status!="CLOSED":blockers.append(f"{row.issue_id}:critical_open")
        payload={"project_id":project_id,"revision":revision,"disciplines":[asdict(x) for x in disciplines],"interfaces":[asdict(x) for x in interfaces],"issues":[asdict(x) for x in issues],"blocking_reasons":blockers}
        digest=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
        return CoordinationSnapshot(project_id,revision,tuple(disciplines),tuple(interfaces),tuple(issues),"READY_FOR_PROFESSIONAL_RELEASE_GATE" if not blockers else "BLOCKED",tuple(blockers),digest)
    def render_html(self,snapshot):
        rows="".join(f"<tr><td>{html.escape(x.discipline)}</td><td>{html.escape(x.model_id)}</td><td>{html.escape(x.revision)}</td><td>{html.escape(x.status)}</td><td>{x.open_issues}</td></tr>" for x in snapshot.disciplines)
        blockers="".join(f"<li>{html.escape(x)}</li>" for x in snapshot.blocking_reasons) or "<li>None — professional release gate still required.</li>"
        return f'''<!doctype html><html><head><meta charset="utf-8"><title>AIAS Coordination</title><style>body{{font:15px system-ui;background:#0b1220;color:#e7edf7;padding:24px}}table{{border-collapse:collapse;width:100%}}td,th{{padding:9px;border:1px solid #34445e}}.status{{font-size:22px}}</style></head><body><h1>AIAS Multidisciplinary Coordination</h1><p>{html.escape(snapshot.project_id)} · {html.escape(snapshot.revision)}</p><p class="status">{html.escape(snapshot.release_readiness)}</p><table><tr><th>Discipline</th><th>Model</th><th>Revision</th><th>Status</th><th>Open issues</th></tr>{rows}</table><h2>Blocking reasons</h2><ul>{blockers}</ul><p>Snapshot SHA-256: {snapshot.snapshot_sha256}</p><p>Professional release is always required.</p></body></html>'''
    def write(self,snapshot,output:Path):
        output.mkdir(parents=True,exist_ok=True);data=output/"AIAS_COORDINATION_SNAPSHOT.json";panel=output/"AIAS_COORDINATION_DASHBOARD.html"
        data.write_text(json.dumps(asdict(snapshot),ensure_ascii=False,indent=2)+"\n",encoding="utf-8");panel.write_text(self.render_html(snapshot),encoding="utf-8")
        return {"snapshot":str(data),"panel":str(panel),"sha256":snapshot.snapshot_sha256,"validated":True}
