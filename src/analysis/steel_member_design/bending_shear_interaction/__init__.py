class BendingShearInteraction:
    def unity(self, moment, moment_capacity, shear, shear_capacity):
        return abs(moment)/moment_capacity + (abs(shear)/shear_capacity)**2
