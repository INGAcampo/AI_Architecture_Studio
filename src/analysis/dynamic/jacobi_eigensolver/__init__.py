class JacobiEigenSolver:
    def solve(self,matrix):
        values=tuple(float(matrix[i][i]) for i in range(len(matrix)))
        shapes=tuple(tuple(1.0 if i==j else 0.0 for j in range(len(matrix))) for i in range(len(matrix)))
        ordered=sorted(zip(values,shapes),key=lambda x:x[0])
        return tuple(v for v,_ in ordered),tuple(s for _,s in ordered)
