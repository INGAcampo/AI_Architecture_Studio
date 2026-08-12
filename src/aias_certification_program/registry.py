"""Official AIAS certification objectives and external authority boundaries."""
from __future__ import annotations


def official_frameworks() -> tuple[dict, ...]:
    """Return the approved certification portfolio without reproducing licensed standards."""
    return (
        {
            "id": "CMMI-DEV-V3-ML5",
            "role": "PRIMARY_ORGANIZATIONAL_MATURITY_OBJECTIVE",
            "target": "CMMI Development V3.0 Maturity Level 5",
            "issuer_or_authority": "CMMI Institute / ISACA appraisal ecosystem",
            "external_decision": "Benchmark appraisal rating led by an active Certified High Maturity Lead Appraiser",
            "current_status": "ADOPTION_AND_EVIDENCE_BUILDING",
            "official_source": "https://cmmiinstitute.com/products/cmmi/content-release",
        },
        {
            "id": "CMMI-AIM",
            "role": "MANDATORY_AI_MATURITY_EXTENSION",
            "target": "CMMI Artificial Intelligence Maturity benchmark view",
            "issuer_or_authority": "CMMI Institute / ISACA appraisal ecosystem",
            "external_decision": "CMMI AIM appraisal led by appropriately certified appraisers; Level 4/5 requires high-maturity qualification",
            "current_status": "ADOPTION_AND_CROSSWALK",
            "official_source": "https://cmmiinstitute.com/news/press-releases/july-2026/cmmi-institute-launches-new-ai-maturity-%28aim%29-model",
        },
        {
            "id": "ISO-9001",
            "role": "QUALITY_MANAGEMENT_CERTIFICATION",
            "target": "ISO 9001:2015/Amd 1:2024, with controlled migration to ISO 9001:2026 after publication",
            "issuer_or_authority": "Independent accredited management-system certification body",
            "external_decision": "Accredited third-party certification audit",
            "current_status": "IMPLEMENTATION_AND_TRANSITION_MONITORING",
            "official_source": "https://www.iso.org/standard/62085.html",
        },
        {
            "id": "ISO-IEC-27001",
            "role": "INFORMATION_SECURITY_CERTIFICATION",
            "target": "ISO/IEC 27001:2022/Amd 1:2024",
            "issuer_or_authority": "Independent accredited management-system certification body",
            "external_decision": "Accredited third-party certification audit",
            "current_status": "IMPLEMENTATION",
            "official_source": "https://www.iso.org/standard/27001",
        },
        {
            "id": "ISO-IEC-42001",
            "role": "AI_MANAGEMENT_CERTIFICATION",
            "target": "ISO/IEC 42001:2023",
            "issuer_or_authority": "Independent certification body competent for AIMS; ISO/IEC 42006:2025 applies to certification bodies",
            "external_decision": "Independent third-party AIMS certification audit",
            "current_status": "IMPLEMENTATION",
            "official_source": "https://www.iso.org/standard/42001",
        },
        {
            "id": "ISO-22301",
            "role": "BUSINESS_CONTINUITY_CERTIFICATION",
            "target": "ISO 22301:2019/Amd 1:2024, monitored for the next edition",
            "issuer_or_authority": "Independent accredited management-system certification body",
            "external_decision": "Accredited third-party certification audit",
            "current_status": "PLANNED_AFTER_CORE_INTEGRATED_SYSTEM",
            "official_source": "https://www.iso.org/standard/75106.html",
        },
    )
