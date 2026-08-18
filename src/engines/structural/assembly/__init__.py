def zeros(n):
    if n < 1: raise ValueError("n debe ser positivo")
    return [[0.0 for _ in range(n)] for _ in range(n)]
class GlobalStiffnessAssembler:
    def __init__(self,dof_count): self.matrix=zeros(dof_count)
    def add_element(self,dofs,local):
        if len(local)!=len(dofs): raise ValueError("Tamaño incompatible")
        for i,gi in enumerate(dofs):
            for j,gj in enumerate(dofs):
                self.matrix[gi][gj]+=local[i][j]
        return self.matrix
