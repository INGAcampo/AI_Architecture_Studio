class StrongColumnWeakBeamEngine:
    def ratio(self,column_moments,beam_moments): return sum(column_moments)/max(sum(beam_moments),1e-12)
    def passes(self,column_moments,beam_moments,minimum=1.2): return self.ratio(column_moments,beam_moments)>=minimum
