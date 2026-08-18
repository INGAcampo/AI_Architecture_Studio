class StrengthCombinationEngine:
    def combine(self, dead, live, wind=0.0):
        return max(1.4*dead, 1.2*dead + 1.6*live + 0.5*wind)
