from __future__ import annotations
from dataclasses import dataclass, asdict, field
import hashlib, json
from typing import Any, Callable

@dataclass
class Finding:
    finding_id: str
    status: str
    severity: str
    message: str
    evidence_sha256: str
    source: str

@dataclass
class QAPackage:
    project_id: str
    findings: list[Finding] = field(default_factory=list)
    score: dict[str, Any] = field(default_factory=dict)
    gate: str = "NOT_READY"
    audit_trail: list[dict[str, Any]] = field(default_factory=list)

class QACore:
    """Deterministic completeness gate and bounded correction loop."""
    def validate(self, graph, standards, analysis_model, analysis_result, drawing_model, quantities, reports) -> QAPackage:
        findings: list[Finding] = []
        def add(status, severity, message, source):
            payload = {"status": status, "severity": severity, "message": message, "source": source}
            fid = "QA-" + hashlib.sha256(message.encode()).hexdigest()[:12]
            findings.append(Finding(fid, status, severity, message, _sha(payload), source))
        if not graph.nodes: add("FAIL", "CRITICAL", "Project Graph has no nodes", "graph")
        ids = {n["id"] for n in graph.nodes}
        if any(r["source"] not in ids or r["target"] not in ids for r in graph.relationships): add("FAIL", "CRITICAL", "orphan BIM relationship", "graph")
        required = {"site", "level", "space"}
        missing = required - {n["type"] for n in graph.nodes}
        if missing: add("INSUFFICIENT_EVIDENCE", "HIGH", f"missing BIM types: {sorted(missing)}", "graph")
        if not analysis_model or not getattr(analysis_model, "members", []): add("INSUFFICIENT_EVIDENCE", "CRITICAL", "analysis model has no members", "analysis")
        if not analysis_result or not getattr(analysis_result, "code_checks", {}): add("FAIL", "CRITICAL", "analysis code checks unavailable", "analysis")
        if not drawing_model or not getattr(drawing_model, "sheets", []): add("FAIL", "HIGH", "drawings unavailable", "drawings")
        if not quantities or not getattr(quantities, "items", []): add("FAIL", "HIGH", "quantities unavailable", "quantities")
        if not reports or not getattr(reports, "documents", {}): add("FAIL", "HIGH", "reports unavailable", "reports")
        if not getattr(standards, "rules", {}): add("INSUFFICIENT_EVIDENCE", "CRITICAL", "standards evidence unavailable", "standards")
        critical = sum(1 for f in findings if f.severity == "CRITICAL" and f.status in {"FAIL", "INSUFFICIENT_EVIDENCE"})
        score = {"total_checks": 8, "findings": len(findings), "critical_blockers": critical, "percent": round(max(0, 100 * (8-len(findings))/8), 2)}
        gate = "READY_FOR_PILOT_ISSUANCE" if critical == 0 and not any(f.status == "FAIL" for f in findings) else "NOT_READY"
        return QAPackage(graph.project_id, findings, score, gate, [{"event": "validation", "finding_count": len(findings), "gate": gate}])

    def design_loop(self, graph, correction: Callable[[Any], None] | None, validate: Callable[[Any], QAPackage], max_iterations: int = 3) -> QAPackage:
        if max_iterations < 1: raise ValueError("max_iterations must be positive")
        trail = []
        for iteration in range(max_iterations):
            result = validate(graph); trail.append({"iteration": iteration, "gate": result.gate, "findings": len(result.findings)})
            if result.gate == "READY_FOR_PILOT_ISSUANCE": result.audit_trail = trail; return result
            if correction is None: result.audit_trail = trail; return result
            before = _sha(graph.to_dict()); correction(graph); after = _sha(graph.to_dict())
            trail.append({"iteration": iteration, "event": "correction_applied", "before": before, "after": after})
            if before == after: result.audit_trail = trail; return result
        result.audit_trail = trail; return result

def _sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, default=str).encode()).hexdigest()
