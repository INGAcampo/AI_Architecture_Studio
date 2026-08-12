from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class StabilityResult:
    maximum_unity: float
    governing: str
    status: str
class StabilityUnity:
    def evaluate(self, axial, axial_cap, mx, mx_cap, my, my_cap):
        ratios={'axial':abs(axial)/max(axial_cap,1e-12),'mx':abs(mx)/max(mx_cap,1e-12),'my':abs(my)/max(my_cap,1e-12)}
        governing=max(ratios,key=ratios.get); value=ratios[governing]
        return StabilityResult(value,governing,'PASS' if value<=1 else 'FAIL')
