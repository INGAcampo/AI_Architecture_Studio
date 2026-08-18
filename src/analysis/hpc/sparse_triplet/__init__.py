class SparseTripletBuilder:
    def __init__(self):self.entries=[]
    def add(self,r,c,v):self.entries.append((r,c,float(v)))
    def compressed(self):
        m={}
        for r,c,v in self.entries:m[(r,c)]=m.get((r,c),0)+v
        return tuple((r,c,v) for (r,c),v in sorted(m.items()))
