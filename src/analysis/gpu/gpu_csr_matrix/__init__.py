class GPUCSRMatrix:
    def __init__(self,indptr,indices,data): self.indptr=tuple(indptr);self.indices=tuple(indices);self.data=tuple(data)
    def matvec(self,x):
        return tuple(sum(self.data[k]*x[self.indices[k]] for k in range(self.indptr[r],self.indptr[r+1])) for r in range(len(self.indptr)-1))
