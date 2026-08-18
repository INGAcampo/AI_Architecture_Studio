class EnergyBalanceEngine:
    def error(self,input_energy,kinetic,strain,damping,contact=0):
        return abs(input_energy-(kinetic+strain+damping+contact))/max(abs(input_energy),1e-12)
