class BlockShearEngine:
    def nominal_strength_n(self, agv, anv, ant, fy, fu):
        r1 = 0.6 * fy * agv + fu * ant
        r2 = 0.6 * fu * anv + fu * ant
        return min(r1, r2)
