"""Reconcile approved historical decisions against current repository evidence."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ALLOWED = {"EVIDENCED", "PARTIAL", "NOT_EVIDENCED", "EXTERNAL_DEPENDENCY"}


class HistoricalDecisionReconciler:
    """Validate historical gap claims and select technical work without erasing external gates."""

    def reconcile(self, root: Path) -> dict:
        root = root.resolve()
        assessment_path = root / "engineering/aias/history/chat01/CHAT01_MATERIALIZATION_GAP.json"
        register_path = root / "engineering/aias/history/chat01/CHAT01_DECISION_REGISTER.json"
        assessment = json.loads(assessment_path.read_text(encoding="utf-8"))
        register = json.loads(register_path.read_text(encoding="utf-8"))
        approved = {item["id"] for item in register["decisions"] if item["status"].startswith("APPROVED")}
        rows, issues = [], []
        for item in assessment["items"]:
            decision_id = item.get("decision_id", "")
            status = item.get("status", "")
            declared = [str(path) for path in item.get("evidence", [])]
            existing = [path for path in declared if (root / path).exists()]
            missing = [path for path in declared if path not in existing]
            if decision_id not in approved:
                issues.append(f"{decision_id}:not_approved")
            if status not in ALLOWED:
                issues.append(f"{decision_id}:invalid_status")
            if status == "EVIDENCED" and missing:
                issues.append(f"{decision_id}:evidence_missing")
            if status == "NOT_EVIDENCED" and declared:
                issues.append(f"{decision_id}:unexpected_evidence")
            rows.append({"decision_id": decision_id, "status": status, "declared_evidence": declared, "verified_evidence": existing, "missing_evidence": missing, "gap": item.get("gap")})
        priority_ids = [text.split(" ", 1)[0] for text in assessment.get("priority_recommendations", [])]
        technical = [item for decision_id in priority_ids for item in rows if item["decision_id"] == decision_id and item["status"] in {"PARTIAL", "NOT_EVIDENCED"}]
        external = [item for item in rows if item["status"] == "EXTERNAL_DEPENDENCY"]
        i18n_foundation = (root / "engineering/aias/internationalization/I18N_CORE_001_SPEC.json").is_file()
        i18n_priority = (root / "engineering/aias/internationalization/I18N_CORE_002_SPEC.json").is_file()
        i18n_main = (root / "engineering/aias/internationalization/I18N_CORE_003_SPEC.json").is_file()
        i18n_workspace = (root / "engineering/aias/internationalization/I18N_CORE_004_SPEC.json").is_file()
        payload = {
            "audit_id": "ROADMAP-RECONCILIATION-002",
            "status": "VALID" if not issues else "INVALID",
            "approved_decisions_assessed": len(rows),
            "counts": {state: sum(item["status"] == state for item in rows) for state in sorted(ALLOWED)},
            "items": rows,
            "technical_priority_queue": [item["decision_id"] for item in technical],
            "external_dependencies": [item["decision_id"] for item in external],
            "deferred_macrodeliveries": ["EXP-COMMS-001"],
            "issues": issues,
            "next": ("I18N-CORE-005 BIM Browser Tree and Remaining Workspace Controls Localization" if i18n_workspace else ("I18N-CORE-004 BIM Inspector and Workspace Model Localization" if i18n_main else ("I18N-CORE-003 Main Window and New Project Localization" if i18n_priority else ("I18N-CORE-002 Prioritized GUI Localization Remediation" if i18n_foundation else "I18N-CORE-001 Internationalization Coverage Audit and Acceptance Suite")))) if technical and technical[0]["decision_id"] == "GEN-009" else None,
        }
        payload["sha256"] = hashlib.sha256(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        return payload

    def write(self, root: Path, output: Path) -> dict:
        """Persist the deterministic reconciliation report."""
        report = self.reconcile(root)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return report
