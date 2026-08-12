from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class InteractionResult:
    axial_ratio: float
    major_ratio: float
    minor_ratio: float
    interaction_ratio: float
    equation: str

class ColumnInteractionEngine:
    def calculate(self, axial, axial_capacity, major_moment, major_capacity, minor_moment, minor_capacity):
        pa=abs(axial)/max(axial_capacity,1e-12)
        mx=abs(major_moment)/max(major_capacity,1e-12)
        my=abs(minor_moment)/max(minor_capacity,1e-12)
        if pa>=0.2:
            interaction=pa+(8.0/9.0)*(mx+my)
            equation="H1-1a"
        else:
            interaction=pa/2.0+mx+my
            equation="H1-1b"
        return InteractionResult(pa,mx,my,interaction,equation)
