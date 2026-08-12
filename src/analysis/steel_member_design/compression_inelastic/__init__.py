import math
class InelasticCompressionEngine:
    def critical_stress_mpa(self, fy_mpa, e_mpa, kl_over_r):
        fe = math.pi**2 * e_mpa / max(kl_over_r**2, 1e-12)
        if kl_over_r <= 4.71 * (e_mpa / fy_mpa) ** 0.5:
            return (0.658 ** (fy_mpa/fe)) * fy_mpa
        return 0.877 * fe
