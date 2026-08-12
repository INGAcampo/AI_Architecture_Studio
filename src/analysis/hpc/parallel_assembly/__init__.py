from analysis.hpc.sparse_triplet import SparseTripletBuilder
class ParallelAssemblyEngine:
    def assemble(self,mats,dofs):
        b=SparseTripletBuilder()
        for m,d in zip(mats,dofs):
            for i,gi in enumerate(d):
                for j,gj in enumerate(d):b.add(gi,gj,m[i][j])
        return b.compressed()
