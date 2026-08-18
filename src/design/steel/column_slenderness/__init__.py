from dataclasses import dataclass
from design.steel.column_domain import BucklingAxis

@dataclass(frozen=True, slots=True)
class SlendernessResult:
    major: float
    minor: float
    critical_axis: BucklingAxis
    maximum: float

class ColumnSlendernessEngine:
    def calculate(self, effective_length_major, effective_length_minor, profile):
        major=effective_length_major/max(profile.rx,1e-12)
        minor=effective_length_minor/max(profile.ry,1e-12)
        axis=BucklingAxis.MAJOR if major>=minor else BucklingAxis.MINOR
        return SlendernessResult(major,minor,axis,max(major,minor))
