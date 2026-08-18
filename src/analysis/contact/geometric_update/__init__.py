class GeometricUpdateEngine:
    def update(self,c,u): return tuple(tuple(a+b for a,b in zip(p,d)) for p,d in zip(c,u))
