"""Executable foundational constitutional articles and their validator bindings."""
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class ConstitutionalArticle:
    """Mandatory governance statement linked to one or more executable validators."""
    article_id: str
    title: str
    statement: str
    mandatory: bool
    validator_ids: tuple[str, ...]

FOUNDATIONAL_ARTICLES = (
    ConstitutionalArticle(
        "AEC-ART-000001",
        "Engineering before implementation",
        "Every production capability shall originate from an approved engineering asset.",
        True,
        ("VAL-SPEC-000001",),
    ),
    ConstitutionalArticle(
        "AEC-ART-000002",
        "Traceability",
        "Every approved requirement shall link to implementation and tests.",
        True,
        ("VAL-TRACE-000001",),
    ),
    ConstitutionalArticle(
        "AEC-ART-000003",
        "Reusable-first",
        "Reusable platform capabilities shall be implemented before duplicated product implementations.",
        True,
        ("VAL-REUSE-000001",),
    ),
    ConstitutionalArticle(
        "AEC-ART-000004",
        "Sustainable acceleration",
        "AEPS shall pursue at least 45 percent reduction in repetitive manual engineering effort without degrading quality.",
        True,
        ("VAL-KPI-000001",),
    ),
)
