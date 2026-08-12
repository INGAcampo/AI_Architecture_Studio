class MassMatrixEngine:
    def lumped(self,masses):
        return tuple(tuple(float(masses[i]) if i==j else 0.0 for j in range(len(masses))) for i in range(len(masses)))
