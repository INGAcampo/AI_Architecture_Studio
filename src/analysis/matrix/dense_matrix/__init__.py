class DenseMatrix:
    def __init__(self,rows): self.rows=[list(r) for r in rows]
    def matvec(self,v): return tuple(sum(a*b for a,b in zip(r,v)) for r in self.rows)
