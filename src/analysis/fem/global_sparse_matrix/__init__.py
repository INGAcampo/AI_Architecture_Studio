class GlobalSparseMatrix:
 def __init__(self,n): self.n=n; self.data={}
 def add(self,i,j,v): self.data[(i,j)]=self.data.get((i,j),0)+v
 def get(self,i,j): return self.data.get((i,j),0)
