from analysis.dynamic.jacobi_eigensolver import JacobiEigenSolver
class GeneralizedEigenEngine:
    def solve(self,stiffness,mass):
        matrix=tuple(tuple(stiffness[i][j]/max(mass[i][i],1e-12) if i==j else 0.0 for j in range(len(stiffness))) for i in range(len(stiffness)))
        return JacobiEigenSolver().solve(matrix)
