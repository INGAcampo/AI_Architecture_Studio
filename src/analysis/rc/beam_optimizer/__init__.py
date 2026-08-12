class BeamOptimizer:
    def lightest_feasible(self,candidates):
        f=[c for c in candidates if c["utilization"]<=1 and c["serviceable"]]
        return min(f,key=lambda c:c["concrete_volume"]+c["steel_mass"]/7850) if f else None
