class CostOptimizer:
    def total_cost(self, mass_kg, unit_cost, fabrication_factor=1.0):
        return mass_kg*unit_cost*fabrication_factor
