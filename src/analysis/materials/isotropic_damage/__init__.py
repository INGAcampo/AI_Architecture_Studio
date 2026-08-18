class IsotropicDamageEngine:
    def degrade(self,s,d): return tuple((1-min(max(d,0),.999999))*v for v in s)
