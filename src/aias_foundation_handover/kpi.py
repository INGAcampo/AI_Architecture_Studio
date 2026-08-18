"""Sustainable-acceleration KPI evidence for ECP-000001F."""
from __future__ import annotations
from .models import KpiEvidence

def calculate(baseline_hours: float, actual_hours: float, automated_hours: float, reused_assets: int, total_assets: int, classification: str = "REFERENCE_ENGINEERING_ESTIMATE") -> KpiEvidence:
    """Calculate time reduction, automation and reuse ratios with validation."""
    if baseline_hours <= 0 or actual_hours < 0 or automated_hours < 0 or actual_hours > baseline_hours: raise ValueError("invalid_time_evidence")
    if total_assets <= 0 or reused_assets < 0 or reused_assets > total_assets: raise ValueError("invalid_reuse_evidence")
    reduction = 1 - actual_hours / baseline_hours
    return KpiEvidence(classification, baseline_hours, actual_hours, automated_hours, reused_assets, total_assets, reduction, automated_hours / actual_hours if actual_hours else 0.0, reused_assets / total_assets, reduction >= .45, "Reference estimate; production Level 5 claims require independently auditable measurements.")
