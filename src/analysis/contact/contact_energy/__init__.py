class ContactEnergyEngine:
    def penalty_energy(self,p,k): return .5*k*max(p,0)**2
