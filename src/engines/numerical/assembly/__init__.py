from dataclasses import dataclass
from engines.numerical.sparse_matrices import SparseMatrixCSR

@dataclass(frozen=True, slots=True)
class ElementMatrixContribution:
    equations:tuple[int|None,...]
    matrix:tuple[tuple[float,...],...]

class GlobalMatrixAssembler:
    def assemble(self,size,contributions):
        triplets=[]
        for c in contributions:
            for i,gi in enumerate(c.equations):
                if gi is None: continue
                for j,gj in enumerate(c.equations):
                    if gj is None: continue
                    triplets.append((gi,gj,c.matrix[i][j]))
        return SparseMatrixCSR.from_triplets(size,size,triplets)
