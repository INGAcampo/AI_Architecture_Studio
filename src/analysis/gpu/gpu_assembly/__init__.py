class GPUAssemblyEngine:
    def assemble(self,mats,dofs,size):
        A=[[0.0]*size for _ in range(size)]
        for m,d in zip(mats,dofs):
            for i,gi in enumerate(d):
                for j,gj in enumerate(d): A[gi][gj]+=m[i][j]
        return tuple(tuple(r) for r in A)
