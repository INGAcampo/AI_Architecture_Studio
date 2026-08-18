from __future__ import annotations

from dataclasses import dataclass

from structural_platform_compare.compare import compare_scalar_results


@dataclass(frozen=True)
class ComparisonRow:
    key: str
    status: str
    baseline: float | None
    candidate: float | None
    absolute_delta: float | None
    relative_delta: float | None


@dataclass(frozen=True)
class ComparisonMatrix:
    rows: tuple[ComparisonRow,...]

    @property
    def mismatch_count(self) -> int:
        return sum(1 for row in self.rows if row.status!="MATCH")


def compare_result_maps(
    baseline: dict[str,float],
    candidate: dict[str,float],
    *,
    abs_tol: float = 1e-9,
    rel_tol: float = 1e-6,
) -> ComparisonMatrix:
    rows=[]

    keys=sorted(set(baseline) | set(candidate))

    for key in keys:
        if key not in baseline:
            rows.append(ComparisonRow(key,"MISSING_BASELINE",None,float(candidate[key]),None,None))
            continue

        if key not in candidate:
            rows.append(ComparisonRow(key,"MISSING_CANDIDATE",float(baseline[key]),None,None,None))
            continue

        result=compare_scalar_results(
            float(baseline[key]),
            float(candidate[key]),
            abs_tol=abs_tol,
            rel_tol=rel_tol,
        )

        status="MATCH" if result.within_tolerance else "MISMATCH"

        rows.append(
            ComparisonRow(
                key,
                status,
                result.baseline,
                result.candidate,
                result.absolute_delta,
                result.relative_delta,
            )
        )

    return ComparisonMatrix(tuple(rows))
