class SteelFatigueProperties:
    def allowable_range_mpa(self,C,N): return (C/max(N,1.))**(1/3)
