class WeightOptimizer:
    def reduction_percent(self, current_mass, proposed_mass):
        return max(0.0,(current_mass-proposed_mass)/current_mass*100.0)
