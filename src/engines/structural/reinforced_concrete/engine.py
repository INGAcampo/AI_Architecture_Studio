class ReinforcedConcreteEngine:
    STEEL_DENSITY=7850
    def steel_volume(self,m): return sum(r.total_area*r.length for r in m.rebars)
    def steel_mass(self,m): return self.steel_volume(m)*self.STEEL_DENSITY
    def ratio(self,m): return self.steel_volume(m)/m.concrete_volume
