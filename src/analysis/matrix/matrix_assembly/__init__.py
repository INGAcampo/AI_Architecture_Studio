class MatrixAssemblyEngine:
    def assemble(self,g,k,dofs):
        for a,i in enumerate(dofs):
            for b,j in enumerate(dofs): g.add(i,j,k[a][b])
        return g
