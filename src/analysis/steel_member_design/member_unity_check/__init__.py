from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class UnityResult:
    maximum_unity: float
    governing: str
    status: str

class MemberUnityCheck:
    def evaluate(self, demands, capacity):
        ratios = {
            "axial": abs(demands.axial_n) / max(capacity.axial_n, 1e-12),
            "mx": abs(demands.mx_nmm) / max(capacity.mx_nmm, 1e-12),
            "my": abs(demands.my_nmm) / max(capacity.my_nmm, 1e-12),
            "shear": abs(demands.shear_n) / max(capacity.shear_n, 1e-12),
        }
        governing = max(ratios, key=ratios.get)
        maximum = ratios[governing]
        return UnityResult(maximum, governing, "PASS" if maximum <= 1.0 else "FAIL")
