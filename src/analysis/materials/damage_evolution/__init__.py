class DamageEvolutionLaw:
    def exponential(self,k,k0,b):
        from math import exp
        return 0.0 if k<=k0 else min(.999999,1-(k0/k)*exp(-b*(k-k0)))
