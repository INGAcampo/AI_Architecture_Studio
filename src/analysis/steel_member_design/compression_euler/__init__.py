import math
class EulerBucklingEngine:
    def critical_load_n(self, e_mpa, i_mm4, k, length_mm):
        return math.pi**2 * e_mpa * i_mm4 / ((k*length_mm)**2)
