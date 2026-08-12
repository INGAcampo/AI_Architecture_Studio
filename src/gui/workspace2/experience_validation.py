"""Automated accessibility/performance gates and honest human-session evidence."""
from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import asdict, dataclass
from pathlib import Path

from aias_design_system import design_tokens, render_qss


def _rgb(value: str) -> tuple[float, float, float]:
    channels = [int(value[index:index + 2], 16) / 255 for index in (1, 3, 5)]
    return tuple(channel / 12.92 if channel <= .04045 else ((channel + .055) / 1.055) ** 2.4 for channel in channels)


def contrast_ratio(foreground: str, background: str) -> float:
    first, second = (_rgb(foreground), _rgb(background))
    light1, light2 = (sum(weight * channel for weight, channel in zip((.2126, .7152, .0722), color)) for color in (first, second))
    return (max(light1, light2) + .05) / (min(light1, light2) + .05)


def audit_design_contrast() -> dict:
    tokens = design_tokens(); pairs = (("text", "background", 4.5), ("text_muted", "background", 4.5), ("on_accent", "accent", 4.5), ("warning", "background", 3.0), ("success", "background", 3.0), ("danger", "background", 3.0))
    results = []
    for theme in ("dark", "light"):
        for foreground, background, minimum in pairs:
            ratio = round(contrast_ratio(tokens[theme][foreground], tokens[theme][background]), 2)
            results.append({"theme": theme, "foreground": foreground, "background": background, "ratio": ratio, "minimum": minimum, "passed": ratio >= minimum})
    return {"schema": "AIAS-CONTRAST-AUDIT-1.0", "results": results, "passed": all(item["passed"] for item in results)}


def audit_html(path: Path, *, maximum_bytes: int = 200_000) -> dict:
    text = path.read_text(encoding="utf-8"); lower = text.casefold(); issues = []
    checks = {
        "doctype": lower.lstrip().startswith("<!doctype html>"),
        "language": bool(re.search(r"<html[^>]+lang=", lower)),
        "utf8": 'charset="utf-8"' in lower,
        "viewport": 'name="viewport"' in lower,
        "single_h1": len(re.findall(r"<h1\b", lower)) == 1,
        "main_landmark": "<main" in lower,
        "responsive_rule": "@media" in lower,
        "professional_boundary": any(term in lower for term in ("professional", "profesional", "licencia", "construction approval")),
        "size_budget": path.stat().st_size <= maximum_bytes,
    }
    issues.extend(name for name, passed in checks.items() if not passed)
    return {"path": str(path), "bytes": path.stat().st_size, "maximum_bytes": maximum_bytes, "checks": checks, "issues": issues, "passed": not issues, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def audit_qss_performance(iterations: int = 250, budget_ms_each: float = 2.0) -> dict:
    started = time.perf_counter()
    for index in range(iterations): render_qss("dark" if index % 2 == 0 else "light")
    elapsed = (time.perf_counter() - started) * 1000; average = elapsed / iterations
    return {"iterations": iterations, "elapsed_ms": round(elapsed, 3), "average_ms": round(average, 4), "budget_ms_each": budget_ms_each, "passed": average <= budget_ms_each}


@dataclass(frozen=True)
class UsabilitySessionEvidence:
    session_id: str
    participant_role: str
    facilitator: str
    observed_at: str
    task_results: tuple[dict, ...]
    consent_reference: str

    def validate(self, required_tasks: tuple[str, ...]) -> list[str]:
        issues = []
        if not all((self.session_id, self.participant_role, self.facilitator, self.observed_at, self.consent_reference)): issues.append("incomplete_session_identity")
        ids = tuple(item.get("task_id") for item in self.task_results)
        if set(ids) != set(required_tasks) or len(ids) != len(set(ids)): issues.append("incomplete_or_duplicate_tasks")
        for item in self.task_results:
            if item.get("outcome") not in {"PASS", "FAIL", "ABANDONED"}: issues.append(f'{item.get("task_id")}:invalid_outcome')
            if not isinstance(item.get("elapsed_seconds"), (int, float)) or item.get("elapsed_seconds", -1) < 0: issues.append(f'{item.get("task_id")}:invalid_elapsed_time')
        return issues

    def snapshot(self) -> dict:
        payload = asdict(self); payload["task_results"] = list(self.task_results)
        payload["sha256"] = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest(); return payload


def build_automated_report(root: Path) -> dict:
    html_paths = (root / "workspace2_w2_04_outputs" / "COMMAND_PALETTE_DARK.png", root / "workspace2_w2_05_outputs" / "LIGHTHOUSE_JOURNEY.html", root / "workspace2_w2_06_outputs" / "COORDINATION_LEARNING.html")
    html_audits = [audit_html(path) for path in html_paths if path.suffix == ".html"]
    contrast = audit_design_contrast(); performance = audit_qss_performance()
    return {"schema": "AIAS-WORKSPACE2-W2-07-AUTOMATED-1.0", "contrast": contrast, "html": html_audits, "qss_performance": performance, "automated_gates_passed": contrast["passed"] and performance["passed"] and all(item["passed"] for item in html_audits), "representative_sessions_completed": 0, "representative_usability_validated": False}
