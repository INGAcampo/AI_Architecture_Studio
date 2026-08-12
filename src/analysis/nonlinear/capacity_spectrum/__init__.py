class CapacitySpectrumEngine:
 def convert(self,v,w,u,factor=1.0):return u*factor,v/max(w*factor,1e-12)
