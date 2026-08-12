def solve_2x2(matrix, vector):
    if len(matrix)!=2 or any(len(row)!=2 for row in matrix) or len(vector)!=2: raise ValueError("Sistema 2x2 requerido")
    det=matrix[0][0]*matrix[1][1]-matrix[0][1]*matrix[1][0]
    if abs(det)<1e-12: raise ValueError("Matriz singular")
    x=(vector[0]*matrix[1][1]-matrix[0][1]*vector[1])/det
    y=(matrix[0][0]*vector[1]-vector[0]*matrix[1][0])/det
    return (x,y)
class LinearStaticSolver:
    def solve(self,matrix,loads): return solve_2x2(matrix,loads)
    def reactions(self,matrix,displacements,loads):
        internal=tuple(sum(matrix[i][j]*displacements[j] for j in range(2)) for i in range(2))
        return tuple(internal[i]-loads[i] for i in range(2))
