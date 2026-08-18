class ShortTermDeflectionEngine:
    def simply_supported_uniform(self,w,L,E,I): return 5*w*L**4/max(384*E*I,1e-12)
