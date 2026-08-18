from dataclasses import dataclass
from engines.numerical.vectors import DenseVector

@dataclass(frozen=True, slots=True)
class SparseMatrixCSR:
    nrows:int
    ncols:int
    indptr:tuple[int,...]
    indices:tuple[int,...]
    data:tuple[float,...]

    def __post_init__(self):
        if len(self.indptr)!=self.nrows+1: raise ValueError("indptr inválido")
        if len(self.indices)!=len(self.data): raise ValueError("Datos inválidos")

    @classmethod
    def from_triplets(cls,nrows,ncols,triplets):
        rows=[{} for _ in range(nrows)]
        for r,c,v in triplets:
            rows[r][c]=rows[r].get(c,0.0)+float(v)
        indptr=[0];indices=[];data=[]
        for row in rows:
            for c in sorted(row):
                if row[c]!=0:
                    indices.append(c);data.append(row[c])
            indptr.append(len(indices))
        return cls(nrows,ncols,tuple(indptr),tuple(indices),tuple(data))

    def matvec(self,vector):
        if len(vector)!=self.ncols: raise ValueError("Dimensiones incompatibles")
        out=[]
        for r in range(self.nrows):
            total=0.0
            for k in range(self.indptr[r],self.indptr[r+1]):
                total+=self.data[k]*vector[self.indices[k]]
            out.append(total)
        return DenseVector(tuple(out))

    @property
    def nnz(self): return len(self.data)
