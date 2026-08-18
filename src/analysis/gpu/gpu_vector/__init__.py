class GPUVectorEngine:
    def add(self,a,b): return tuple(x+y for x,y in zip(a,b))
    def dot(self,a,b): return sum(x*y for x,y in zip(a,b))
