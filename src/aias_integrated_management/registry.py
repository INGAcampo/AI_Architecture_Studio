"""High-level control families shared by the approved certification targets."""
from __future__ import annotations


def control_families() -> tuple[dict, ...]:
    """Return non-clause-level control families without reproducing licensed standards."""
    return (
        {"id": "IMS-CONTEXT", "name": "Context and interested parties", "domains": ("QUALITY", "INFORMATION_SECURITY", "AI_MANAGEMENT", "BUSINESS_CONTINUITY")},
        {"id": "IMS-LEADERSHIP", "name": "Leadership, policy and accountability", "domains": ("QUALITY", "INFORMATION_SECURITY", "AI_MANAGEMENT", "BUSINESS_CONTINUITY")},
        {"id": "IMS-RISK", "name": "Risk and opportunity management", "domains": ("QUALITY", "INFORMATION_SECURITY", "AI_MANAGEMENT", "BUSINESS_CONTINUITY")},
        {"id": "IMS-SUPPORT", "name": "Resources, competence, communication and documented information", "domains": ("QUALITY", "INFORMATION_SECURITY", "AI_MANAGEMENT", "BUSINESS_CONTINUITY")},
        {"id": "IMS-OPERATION", "name": "Operational planning and controlled delivery", "domains": ("QUALITY", "INFORMATION_SECURITY", "AI_MANAGEMENT", "BUSINESS_CONTINUITY")},
        {"id": "IMS-PERFORMANCE", "name": "Monitoring, internal audit and management review", "domains": ("QUALITY", "INFORMATION_SECURITY", "AI_MANAGEMENT", "BUSINESS_CONTINUITY")},
        {"id": "IMS-IMPROVEMENT", "name": "Nonconformity, corrective action and continual improvement", "domains": ("QUALITY", "INFORMATION_SECURITY", "AI_MANAGEMENT", "BUSINESS_CONTINUITY")},
    )
