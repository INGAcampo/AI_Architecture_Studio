class GPUDenseMatrix:
    def matvec(self,A,x): return tuple(sum(a*b for a,b in zip(row,x)) for row in A)
